# This file defines all the handlers and associated routines that are used by the savewhatyoulookedat application.
# The handlers defined in this file are called when the path to a requested resource matches one of the entries in 
# DJango's urlconf file. The routines prefixed by an underscore character are for use inside this file. They are 
# not intended to be used outside this file.
#
# -- Supriyo.

import os
import sys
from re import *
import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import MySQLdb
import time
import md5
from urldbapp.savewhatyoulookedat.forms import *
from urldbapp.savewhatyoulookedat.constants import *
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup

html_escape_table = {"&" : "&amp;", '"' : "&quot;", "'" : "&apos;", ">" : "&gt;", "<" : "&lt;", "\n" : " "}

def html_escape(text):
    return "".join(html_escape_table.get(c, c) for c in text)

def html_unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    s = s.replace("&perc;", "%")
    s = s.replace("&nbsp;", " ")
    return s

# User login handler
def userLogin(request):
    userid, passwd = "", ""
    session_str = ""
    htmlContent = ""
    status_msg = ""
    hostname = request.META["HTTP_HOST"]
    if request.method == "POST":
	userid = request.POST["userid"]
	passwd = request.POST["passwd"]
	if type(userid).__name__ == "NoneType":
	    userid = ""
	if type(passwd).__name__ == "NoneType":
	    passwd = ""
	if userid == "" or passwd == "":
	    status_msg = "One or more fields had no data.<br>Please type in your user ID and password carefully and try again."
	    html = LoginForm(hostname, status_msg, request.POST)
	    return HttpResponse(html)
	else:
	    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
	    authSQL = "select count(*) from savewhatyoulookedat_users where userID='" + userid + "' and password='" + passwd + "'"
	    authCursor = dbconn.cursor()
	    authCursor.execute(authSQL)
	    matchedRecs = authCursor.fetchall()
	    if matchedRecs[0][0] == 0:
		status_msg = "The user ID or the password (or both) you entered is invalid.<br> Please type in your user ID and password carefully and try again.<br>"
		html = LoginForm(hostname, status_msg, request.POST)
		return HttpResponse(html)
	    else:
		t = time.time()
		sess = md5.md5(t.__str__())
		session_str = sess.hexdigest()
		status_msg = "<font color='#0000FF'>You have been logged in as " + userid + "</font><br>"
		cur_time = datetime.datetime.now().__str__()
		start_time, sec_fraction = cur_time.split(".")
		user_data_dir = USER_ROOT_DIR + userid + "/" + session_str + "/data/"
		user_images_dir = USER_ROOT_DIR + userid + "/" + session_str + "/images/"
		# For every session, we create a directory with the sessionid as name in user's data and images directories.
		os.mkdir(USER_ROOT_DIR + userid + "/" + session_str, 0777)
		os.mkdir(user_data_dir, 0777) # This will store data if the user uploads any.
		os.mkdir(user_images_dir, 0777) # This will store images of the pages that the user bookmarks.
		sessionStartSQL = "insert into savewhatyoulookedat_session (sessionID, user_id, startTime, sessionState) values ('" + session_str + "', '" + userid + "', '" + start_time + "', '1')" # 1 indicates an active user.
		authCursor.execute(sessionStartSQL)
		# Session created... now we need to pass this sessionID to the user.
    elif request.method == "GET":
	status_msg = ""
	html = LoginForm(hostname, status_msg)
	return(HttpResponse(html))
    else:
	status_msg = "<b><font color='#FF0000'>Invalid Request</font></b>" # We don't want folks to directly access this script by typing in its URL in a browser window.

    html = LandingPage(userid, session_str, status_msg, request.POST)
    return HttpResponse(html)

# User registration handler
def userRegister(request):
    error_msg = ""
    html = ""
    if request.method == "GET":
	html = RegistrationForm(request.META["HTTP_HOST"], "")
    else:
	firstname = request.POST.get("fname", "")
	middleinitials = request.POST.get("minit", "")
	lastname = request.POST.get("lname", "")
	userid = request.POST.get("userid", "")
	passwd = request.POST.get("passwd", "")
	passwd2 = request.POST.get("passwd2", "")
	emailid = request.POST.get("emailid", "")
	if passwd != passwd2:
	    error_msg = "The 'Password' and 'Retype Password' fields do not match. <br>Please enter exactly same value in both fields."
	    html = RegistrationForm(request.META["HTTP_HOST"], error_msg, request.POST)
	else:
	    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
	    regcursor = dbconn.cursor()
	    # First, check if we already have an user with the same UserID
	    checkSQL = "select count(*) from savewhatyoulookedat_users where userid = '" + userid + "'"
	    regcursor.execute(checkSQL)
	    recs = regcursor.fetchall()
	    if recs[0][0] > 0:
		error_msg = "An user with the same user ID ('" + userid + "') already exists in our database.<br>Please enter a different user ID and try again."
		html = RegistrationForm(request.META["HTTP_HOST"], error_msg, request.POST)
	    else: # First thing: create an images directory and a data directory for the user.
		if not os.path.isdir(USER_ROOT_DIR):
		    os.mkdir(USER_ROOT_DIR, 0777) # Create USER_ROOT_DIR if it didn't exist
		os.mkdir(USER_ROOT_DIR + userid, 0777) # Create directory to store user's data and images.
		curtime = datetime.datetime.now().__str__()
		instime, secFraction = curtime.split(".")
		registerSQL = "insert into savewhatyoulookedat_users (firstName, middleInitials, lastName, userID, emailID, password, createtime) values ('" + firstname + "', '" + middleinitials + "', '" + lastname + "', '" + userid + "', '" + emailid + "', '" + passwd + "', '" + instime + "')"
		regcursor.execute(registerSQL)
		status_msg = "Congrats! You have successfully registered yourself on SaveWhatYouLookedAt.com<br>Please login to start saving website URLs."
		html = RegistrationSuccessful(request.META["HTTP_HOST"], status_msg)
    return HttpResponse(html)

# Save URL handler
def saveURL(request):
    status_msg = ""
    html = ""
    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
    insertUrlCursor = dbconn.cursor()
    if request.method == "GET":
	html = SaveURLForm(request.META["HTTP_HOST"], status_msg, request.GET)
    elif request.method == "POST":
	vURL = request.POST.get("vURL", "")
	vURL = vURL.decode()
	bookmark = request.POST.get("bookmark", "")
	userid = request.POST.get("userid", "")
	sessid = request.POST.get("sessid", "")
	category = request.POST.get("category", "")
	cmdName = request.POST.get('commandName', '')
	cmdArgs = request.POST.get('commandArgs', '')
	if cmdName == "edit":
	    userid = request.POST.get("user", "")
	    sessid = request.POST.get("session", "")
	userid = userid.strip(" ")
	sessid = sessid.strip(" ")
	# Now, do a sanity check...
	error_condition = 0
	if not _isSessionValid(userid, sessid):
	    status_msg = "<font color='#FF0000'>You must be signed in to avail of this feature.<br></font>"
	    html = SaveURLForm(request.META["HTTP_HOST"], status_msg)
	    return HttpResponse(html)
	else:
	    if cmdName != "edit":
		status_msg = "<font color='#0000FF'>Your URL has been saved.<br></font>"
	    fieldsDict = {"userid" : userid, "sessid" : sessid}
	    if cmdName == "edit":
		fieldsDict["commandName"] = cmdName
		fieldsDict["commandArgs"] = cmdArgs
		html = SaveURLForm(request.META["HTTP_HOST"], status_msg, fieldsDict)
	    elif cmdName == "save":
		try:
		    url_html = urllib2.urlopen(vURL).read()
		except:
		    url_html = "Could not retrieve html from " + vURL
		bsoup = BeautifulSoup(url_html)
		imglist = bsoup.findAll("img")
		imgliststr = ""
		if imglist.__len__() > 0:
		    images = _downloadImagesFromWeb(userid, sessid, vURL, imglist)
		    imgliststr = ",".join(images)
		emailslist = bsoup.findAll("mailto:")
		emailslist_str = ",".join(emailslist)
		emailslist2 = _extractEmailIDsfromContent(url_html)
		emailslist2_str = ",".join(emailslist2)
		if emailslist.__len__() > 0:
		    emailslist_str = emailslist_str + "," + emailslist2_str
		else:
		    emailslist_str = emailslist2_str
		currentime = datetime.datetime.now().__str__()
		curtimestamp, secFraction = currentime.split(".")
		sqlcursor = insertUrlCursor
		editRecordSQL = "update savewhatyoulookedat_urls set savedURL='" + vURL + "', bookmark='" + bookmark + "', categoryID='" + category + "', accesstime='" + curtimestamp + "', html='" + url_html + "', images='" + imgliststr + "', emailID_list='" + emailslist_str + "' where urlID='" + cmdArgs + "'"
		sqlcursor.execute(editRecordSQL)
		html = SaveURLForm(request.META["HTTP_HOST"], status_msg, fieldsDict)
	    else:
		if vURL.strip(" ") == "":
		    status_msg = "URL value is missing!"
		    error_condition = 1
		elif category.strip(" ") == "":
		    status_msg = "Category value is missing"
		    error_condition = 1
		else:
		    pass
		if bookmark == "":
		    t = time.time()
		    left, right = t.__str__().split(".")
		    bookmark = userid + left # If bookmark is not entered by the user, we generate one using the userid and time values.
		else:
		    pass
		# Now retrieve HTML content, images and email IDs from the location pointed to by the URL which the user wants to save.
		try:
		    url_html = urllib2.urlopen(vURL).read()
		except:
		    url_html = "Could not retrieve html from " + vURL
		bsoup = BeautifulSoup(url_html)
		imglist = bsoup.findAll("img")
		imgliststr = ""
		if imglist.__len__() > 0:
		    images = _downloadImagesFromWeb(userid, sessid, vURL, imglist)
		    imgliststr = ",".join(images)
		emailslist = bsoup.findAll("mailto:")
		emailslist_str = ",".join(emailslist)
		emailslist2 = _extractEmailIDsfromContent(url_html)
		emailslist2_str = ",".join(emailslist2)
		if emailslist.__len__() > 0:
		    emailslist_str = emailslist_str + "," + emailslist2_str
		else:
		    emailslist_str = emailslist2_str
		currentime = datetime.datetime.now().__str__()
		curtimestamp, secFraction = currentime.split(".")
		# Now insert all this data into the database
		urlInsertSQL = "insert into savewhatyoulookedat_urls (user_id, savedURL, html, images, accesstime, categoryID, sessionID, recieveinfo, bookmark, emailID_list) values ('" + userid + "', '" + vURL + "', '" + url_html + "', '" + imgliststr + "', '" + curtimestamp + "', '" + category + "', '" + sessid + "', '0', '" + bookmark + "', '" + emailslist_str + "')"
		insertUrlCursor.execute(urlInsertSQL) # there... done!
		html = SaveURLForm(request.META["HTTP_HOST"], status_msg, fieldsDict)
    else:
	html = "Invalid method."
    return HttpResponse(html)

# Firefox extension download handler
def firefoxPluginDownload(request):
    PluginPath = "/home/supmit/work/odesk/PythonFirefoxExtn/saveurl.xpi"
    response = HttpResponse(mimetype='text/html')
    if _isSessionValid(request.GET.get("user_id", ""), request.GET.get("session_id", "")):
	response = HttpResponse(mimetype='application/x-www-form-urlencoded')
	response['Content-Disposition'] = "attachment;filename=savewhatyoulookedat.xpi"
	fbh = open(PluginPath, "rb")
	xpiContent = fbh.read()
	fbh.close()
	response.write(xpiContent)
    else:
	status_msg = "You need to register on this site to be able to download the plugin.<br>"
	html = LandingPage(request.GET.get("user_id", ""), request.GET.get("session_id", ""), status_msg)
	response.write(html)
    return response


# User resources view will allow an user to view the URLs stored by her/him along with the 
# choice of category, bookmark name and links to the html textual content, images, emailid 
# list and other similar resources from the webpage pointed to by the URL. On clicking the
# link to textual content or image or email ID list, the content pointed to by it will be 
# displayed in a popup window. Users will be allowed to modify bookmark names. They will 
# be provided with a mechanism to delete an entry too. The rest of the resources will be 
# accessible to them in read-only mode only.

# Session termination handler
def userLogout(request):
    userid = request.POST.get("userid", "")
    sessid = request.POST.get("sessid", "")
    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
    logoutCursor = dbconn.cursor()
    logoutSQL = "update savewhatyoulookedat_session set sessionState=0 where sessionID='" + sessid + "' and user_id='" + userid + "'"
    logoutCursor.execute(logoutSQL)
    message = "You have been successfully logged out. The session has been terminated."
    return HttpResponse(message)

# Function to check if a session is valid. This is not a handler.
# It will be called from within the handler methods defined in this
# file. This is for internal use only. It takes an userid and a 
# session ID as arguments and returns boolean true if the session is
# valid and false otherwise. Ideally, this function should not have
# been declared in this file, since this file is supposed to contain
# request handlers only. However, the isSessionValid() function is 
# mostly used by the handlers defined here and hence, for the sake
# of convenience, I have defined it here. Also, it will save the 
# trouble of importing another file if it is kept here rather than
# in another file.
def _isSessionValid(userid, sessionid):
    if userid.strip(" ") == "" or sessionid.strip(" ") == "":
	return False
    checkSessionValiditySQL = "select sessionState from savewhatyoulookedat_session where sessionID='" + sessionid + "' and user_id='" + userid + "' and DATEDIFF(now(), startTime) <= 1"
    # Rule: A session can remain valid for a day only. This might be made configurable later on.
    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
    validityCursor = dbconn.cursor()
    validityCursor.execute(checkSessionValiditySQL)
    fetchedRecords = validityCursor.fetchall()
    try:
	if fetchedRecords[0][0] == 1:
	    return(True)
	else:
	    return(False)
    except:
	return(False)

# Data management handler (Viewer component)
def manageData(request):
    userid = request.GET.get('user', '')
    sessid = request.GET.get('session', '')
    execstatus = request.GET.get('execstatus', '')
    status_msg = ""
    if execstatus == '1':
	status_msg = "The selected records have been deleted successfully"
    elif execstatus == '0':
	status_msg = "Savewhatyoulookedat.com has detected a problem with your session. There are many reasons for which this might occur. Possibly, your session has been timed out or has got corrupt due to some network disturbance. Please login and try again. <br> If the problem persists, please report this to the system administrator of this website."
    elif execstatus == '2':
	status_msg = "The custom category has been added successfully."
    else:
	pass
    manageDataContent = manageDataFormHeader(userid, sessid, status_msg)
    manageDataContent += manageDataTableHeader(userid, sessid)
    categoryDict = {} # This will be a dictionary that maps category IDs to category names.
    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
    retrieveUrlCursor = dbconn.cursor()
    categorySQL = "select categoryID, categoryname from savewhatyoulookedat_category where userID='" + userid + "' or userID=''"
    retrieveUrlCursor.execute(categorySQL)
    catrecs = retrieveUrlCursor.fetchall()
    for cat in catrecs:
	categoryDict[cat[0]] = cat[1]
    # Retrieve all saved URLs and associated data..."tableRecords" list will contain the resultset.
    retrieveUrlSQL = "select savedURL, html, images, categoryID, bookmark, recieveinfo, accesstime, urlID, sessionID, emailID_list from savewhatyoulookedat_urls where user_id='" + userid + "' order by accesstime desc"
    retrieveUrlCursor.execute(retrieveUrlSQL)
    tableRecords = retrieveUrlCursor.fetchall()
    tableRowContentHolder = manageDataTableRow(userid, sessid)
    serialCounter = 1
    for rec in tableRecords:
	manageDataContentHolder = tableRowContentHolder
	savedURL = rec[0]
	html = rec[1]
	images = "None"
	if rec[2].__len__() > 0:
	    images = rec[2]
	categoryID = rec[3]
	categoryName = categoryDict[categoryID]
	bookmark = rec[4]
	recieveinfo = rec[5]
	accesstime = rec[6]
	urlid = rec[7]
	accessSessID = rec[8]
	emailids = rec[9]
	if emailids == "" or emailids == 'NULL':
	    emailids = None
	if recieveinfo == '1':
	    recieveinfo = "Enabled"
	else:
	    recieveinfo = "Disabled"
	if images != "None":
	    imagePath = "/" + accessSessID + "/images/" +  _getSiteNameFromURL(savedURL) + "/"
	    images = _addLinksToImages(userid, sessid, imagePath, images)
	first30Chars = html[0:30]
	manageDataContent += manageDataContentHolder%(urlid, serialCounter, savedURL, categoryName, bookmark, html_escape(html), html_escape(first30Chars) + " ...[more]", images, emailids, accesstime, recieveinfo, urlid, urlid)
	serialCounter += 1
    
    manageDataContent += manageDataFormFooter(userid, sessid)
    return HttpResponse(manageDataContent)

# Data management handler (Updation component)
def executeCommand(request):
    cmdName = request.POST.get("commandName", "")
    cmdArgs = request.POST.get("commandArgs", "")
    userid = request.POST.get("user", "")
    sessid = request.POST.get("session", "")
    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
    sqlCursor = dbconn.cursor()
    redirectURL = "/savewhatyoulookedat/managedata/?user=" + userid + "&session=" + sessid + "&execstatus="
    if not _isSessionValid(userid, sessid):
	redirectURL += "0"
    else:
	if cmdName == "delete":
	    cmdArgs = cmdArgs.strip()
	    deleteSQL = "delete from savewhatyoulookedat_urls where urlID in (" + cmdArgs + ")"
	    sqlCursor.execute(deleteSQL)
	    redirectURL += "1"
	elif cmdName == "addcat":
	    customCategory = cmdArgs.strip()
	    addCatSQL = "insert into savewhatyoulookedat_category (categoryname, userID) values ('" + customCategory + "', '" + userid + "')"
	    sqlCursor.execute(addCatSQL)
	    redirectURL += "2"
    return HttpResponseRedirect(redirectURL)

def _getSiteNameFromURL(url):
    siteParts = url.split("/")
    siteName = siteParts[2].replace(".", "_") # This is expected to be of the form www.site-name.com.
    siteName = siteName.replace("-", "")
    return(siteName)

def _downloadImagesFromWeb(userid, sessid, url, imagesList):
    destinationPath = USER_ROOT_DIR + userid + "/" + sessid + "/images/" +  _getSiteNameFromURL(url)
    if not os.path.isdir(destinationPath):
	os.mkdir(destinationPath, 0777)
    baseurl = _getBaseURL(url)
    images = []
    webrooturlpat = re.compile("^\/\w+")
    relurlpat = re.compile("^\w[\w\-\.\/_]*$")
    imgctr = 1
    for img in imagesList:
	src = img.get("src")
	if webrooturlpat.match(src):
	    src = baseurl + src
	elif relurlpat.match(src):
	    src = baseurl + _getPathFromURL(url) + "/" + src
	else:
	    pass
	imgfilename = "0000" + imgctr.__str__()
	imgctr += 1
	if JPGPAT.match(src):
	    imgfilename = imgfilename + ".jpg"
	elif GIFPAT.match(src):
	    imgfilename = imgfilename + ".gif"
	elif PNGPAT.match(src):
	    imgfilename = imgfilename + ".png"
	elif BMPPAT.match(src):
	    imgfilename = imgfilename + ".bmp"
	elif TIFFPAT.match(src):
	    imgfilename = imgfilename + ".tiff"
	else:
	    imgfilename = imgfilename + ".jpg" # If we can't find the image file type, we assume it to be jpg.
	images.append(imgfilename)
	imgout = open(destinationPath + "/" + imgfilename, 'w')
	imgcontent = urllib2.urlopen(src).read()
	imgout.write(imgcontent)
	imgout.close()

    return(images)

def _getBaseURL(url):
    siteParts = url.split("/")
    baseurl = siteParts[0] + "//" + siteParts[2]
    return(baseurl)

def _getPathFromURL(url):
    siteParts = url.split("/")
    siteParts.pop()
    urlpath = "/" + "/".join(siteParts[3:])
    return(urlpath)

# Handler to display downloaded images.
def showImage(request):
    userid = request.GET.get("userid", "")
    sessid = request.GET.get("sessid", "")
    imgpath = request.GET.get("imgp", "")
    response = HttpResponse(mimetype='text/html')
    html = ""
    if not _isSessionValid(userid, sessid):
	status_msg = "<font color='#FF0000'>Your session has expired.<br> Please login again before trying to view the desired resource.</font>"
	html = LandingPage(userid, sessid, status_msg)
	response.write(html)
    else:
	imagePath = USER_ROOT_DIR + userid + imgpath
	imgin = open(imagePath, 'r')
	imgcontent = imgin.read()
	imgin.close()
	if JPGPAT.match(imgpath):
	    response = HttpResponse(mimetype='image/jpeg')
	elif GIFPAT.match(imgpath):
	    response = HttpResponse(mimetype='image/gif')
	elif PNGPAT.match(imgpath):
	    response = HttpResponse(mimetype='image/png')
	elif BMPPAT.match(imgpath):
	    response = HttpResponse(mimetype='image/bmp')
	elif TIFFPAT.match(imgpath):
	    response = HttpResponse(mimetype='image/tiff')
	else:
	    response = HttpResponse(mimetype='image/jpeg')
	response.write(imgcontent)
    return(response)

def _addLinksToImages(userid, sessid, imagepath, images):
    imageslist = images.split(",")
    imagelinks = []
    for img in imageslist:
	img.strip(" ")
	alink = """<a href='#' onClick="javascript:showImage('""" + imagepath + img + """', '""" + userid + """', '""" + sessid + """');">""" + img + """</a>"""
	imagelinks.append(alink)
    return ",".join(imagelinks)


def _extractEmailIDsfromContent(html):
    el_list = re.findall(EMAILPAT, html)
    fixed_el_list = []
    for el in el_list:
	if el[el.__len__() - 1] == '.':
	    el = el.strip(".")
	    fixed_el_list.append(el)
    return(fixed_el_list)

# Note: If a search field returns a zero length string, then we ignore that 
# field along with the logic operator preceding it. An exception to this rule
# is the case if the first search field (named "searchBookmark") is a zero
# length string. In that case we will ignore the logic operator immediately
# succeeding it (i.e. "BookmarkLogicURL" field).
# Search request handler
def searchURL(request):
    searchResultset = []
    userid = request.GET.get("userid", "")
    sessid = request.GET.get("sessid", "")
    paramsDict = request.GET
    if request.method == "POST":
	userid = request.POST.get("userid", "")
	sessid = request.POST.get("sessid", "")
	if not _isSessionValid(userid, sessid):
	    status_msg = "<center><b><font color='#FF0000'>You must be logged in to view this page.</font></b></center>"
	    searchHTML = getSearchHeader(userid, sessid, paramsDict)
	    searchHTML += status_msg
	    searchHTML += getSearchForm(userid, sessid, paramsDict)
	    searchHTML += getSearchFooter()
	    return HttpResponse(html_unescape(searchHTML))
	catnametoidmap, catidtonamemap = _getCategoriesMaps(userid)
	paramsDict = request.POST
	searchBookmark = request.POST.get("searchBookmark", "")
	searchURL = request.POST.get("searchURL", "")
	searchCategory = request.POST.get("searchCategory", "")
	searchContent = request.POST.get("searchContent", "")
	searchDate = request.POST.get("searchDate", "")
	BookmarkLogicURL = request.POST.get("BookmarkLogicURL", "")
	URLLogicCategory = request.POST.get("URLLogicCategory", "")
	CategoryLogicContent = request.POST.get("CategoryLogicContent", "")
	ContentLogicDate = request.POST.get("ContentLogicDate", "")
	searchSQL = "select urlID, savedURL, bookmark, html, accesstime, categoryID, recieveinfo, sessionID, images, emailID_list from savewhatyoulookedat_urls where user_id='" + userid + "'"
	if searchBookmark.__len__() > 0:
	    searchSQL += " AND (bookmark like '%" + searchBookmark + "%'"
	else:
	    searchSQL += " AND (bookmark='*'"
	if searchURL.__len__() > 0:
	    searchSQL += " " + BookmarkLogicURL + " savedURL like '%" + searchURL + "%'"
	if searchCategory.__len__() > 0:
	    try:
		searchSQL += " " + URLLogicCategory + " categoryID='" + catnametoidmap[searchCategory] + "'"
	    except KeyError:
		pass
	if searchContent.__len__() > 0:
	    searchSQL += " " + CategoryLogicContent + " html like '%" + searchContent + "%'"
	if searchDate.__len__() > 0:
	    searchSQL += " " + ContentLogicDate + " accesstime like '" + searchDate + "%'"
	searchSQL += ") order by urlID desc" # Sorting by urlID is equivalent to sorting by accesstime but it is much faster.
	dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
	searchCursor = dbconn.cursor()
	searchCursor.execute(searchSQL)
	searchRecords = searchCursor.fetchall()
	for rec in searchRecords:
	    record = {}
	    record["urlID"] = rec[0]
	    record["savedURL"] = rec[1]
	    record["bookmark"] = rec[2]
	    contenthtml = rec[3]
	    record["html"] = html_escape(contenthtml)
	    record["title"] = record["html"]
	    htmlsoup = BeautifulSoup(contenthtml)
	    pgtitle = htmlsoup.findAll("title")
	    if pgtitle.__len__() > 0:
		record["title"] = pgtitle[0].string
	    record["accesstime"] = rec[4]
	    try:
		record["categoryName"] = catidtonamemap[rec[5].__str__()]
	    except KeyError:
		record["categoryName"] = ""
	    record["recieveinfo"] = rec[6]
	    record["accessSessionID"] = rec[7]
	    record["images"] = rec[8]
	    record["emailID_list"] = rec[9]
	    searchResultset.append(record)
    searchHTML = getSearchHeader(userid, sessid, paramsDict)
    searchHTML += getSearchForm(userid, sessid, paramsDict)
    if searchResultset.__len__() > 0:
	searchHTML += searchResultsBody(userid, sessid, searchResultset)
    searchHTML += getSearchFooter()
    return HttpResponse(html_unescape(searchHTML))

# The following function extracts "category" information from database and
# creates a python dictionary with category ID as keys and category names as
# values for a specific user. The userID of the user is passed as an argument.
def _getCategoriesMaps(userid):
    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
    categoriesSQL = "select categoryID, categoryname from savewhatyoulookedat_category where userID='" + userid + "' or userID=''"
    catCursor = dbconn.cursor()
    catCursor.execute(categoriesSQL)
    catrecords = catCursor.fetchall()
    catnametoIDmap = {}
    catIDtonamemap = {}
    for rec in catrecords:
	catid = rec[0].__str__()
	catname = rec[1]
	catnametoIDmap[catname] = catid
	catIDtonamemap[catid] = catname
    return((catnametoIDmap, catIDtonamemap))
