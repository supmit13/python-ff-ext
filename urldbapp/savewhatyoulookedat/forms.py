# This file defines the user interfaces (web interfaces, more precisely). These interfaces are called from the
# savewhatyoulookedat handlers file (which resides in the same directory as this file and named "handlers.py").
# I have tried to use as less python code as is possible in this file. Ideally, this file should not contain any
# python code. However, you will still find that there are places where I have used it quite liberally. I have 
# done this to separate interface logic from the handlers logic, so that it is easier to anyone (other than myself)
# to read and understand the code quickly.
#
# -- Supriyo.

import os
import sys
import re
import datetime
import MySQLdb
from urldbapp.savewhatyoulookedat.constants import *

def RegistrationForm(hostname = "localhost:8000", error_msg = "", fieldsDict = {}):
    registrationForm = """<html><head>
	<title>SaveWhatYouLookedAt.com - Registration Form</title>
	<script Language='JavaScript'>
	String.prototype.trim = function() {
	    a = this.replace(/^\s+/, '');
	    return a.replace(/\s+$/, '');
	};

	function validateInput(){
	    if(document.frmRegister.fname.value.trim() == "" || document.frmRegister.lname.value.trim() == "" || document.frmRegister.userid.value.trim() == "" || document.frmRegister.passwd.value.trim() == "" || document.frmRegister.passwd2.value.trim() == ""){
		alert("One or more 'required' fields are empty. Please fill them up and try again.");
		return(false);
	    }
	    // Now check if any of the 'required' fields have invalid characters
	    var validCharactersList = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_";
	    var userID = document.frmRegister.userid.value.trim();
	    var firstname = document.frmRegister.fname.value.trim();
	    var lastname = document.frmRegister.lname.value.trim();
	    for(var i=0; i < userID.length; i++){
		if(validCharactersList.indexOf(userID.charAt(i)) == -1){
		    alert("User ID field may contain alphanumeric characters only.");
		    document.frmRegister.userid.value = "";
		    document.frmRegister.userid.focus();
		    return(false);
		}
	    }
	    for(var i=0; i < firstname.length; i++){
		if(validCharactersList.indexOf(firstname.charAt(i)) == -1){
		    alert("Firstname field may contain alphanumeric characters only.");
		    document.frmRegister.fname.value = "";
		    document.frmRegister.fname.focus();
		    return(false);
		}
	    }
	    for(var i=0; i < lastname.length; i++){
		if(validCharactersList.indexOf(lastname.charAt(i)) == -1){
		    alert("Lastname field may contain alphanumeric characters only.");
		    document.frmRegister.lname.value = "";
		    document.frmRegister.lname.focus();
		    return(false);
		}
	    }
	    // Password field should contain at least 6 characters
	    var password = document.frmRegister.passwd.value.trim();
	    if(password.length < 6){
		alert("Password should be atleast 6 characters long");
		document.frmRegister.passwd.value="";
		document.frmRegister.passwd.focus();
		return(false);
	    }
	    return(true);
	}

	function submitRegistration(){
	    if(validateInput()){
		document.frmRegister.action = "http://""" + hostname + """/savewhatyoulookedat/register/";
		document.frmRegister.method = "POST";
		document.frmRegister.submit();
	    }
	}
	</script>
	<STYLE type=text/css>BODY {
	    MARGIN: 26px 0px; BACKGROUND-COLOR: #f2f2f2
	}
	</STYLE>
	<LINK href="css/main.css" type=text/css rel=stylesheet><!-- InstanceBeginEditable name="head" --><!-- InstanceEndEditable -->
	<LINK href="css/forms.css" type=text/css rel=stylesheet>
	</head>
	<body bgcolor='#5588BB'>
	<center><h3>Register Now</h3><br><i><b>(Please note that the fields marked with an asterisk are required)</b></i></center>
	<div class='alignleft'></div>
	<div class='alignright'></div>
	<form name='frmRegister' method='POST' action='http://""" + hostname + """/savewhatyoulookedat/register/'>
	<center><font color='#FF0000'><b>""" + error_msg + """</b></font><table border='0' cellspacing='2' cellpadding='2' width='80%'>
	<tr><td align='center'><b>*&nbsp;First&nbsp;&nbsp;Name:</b></td><td><input type='text' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' name='fname' size='30' maxlength='100' value='""" + fieldsDict.get('fname', '') + """'></td></tr>
	<tr><td align='center'><b>&nbsp;Middle&nbsp;Initials:</b></td><td><input type='text' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' name='minit' size='30' value='""" + fieldsDict.get('minit', '') + """'></td></tr>
	<tr><td align='center'><b>*&nbsp;Last&nbsp;&nbsp;Name:</b></td><td><input type='text' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' name='lname' size='30' maxlength='100' value='""" + fieldsDict.get('lname', '') + """'></td></tr>
	<tr><td align='center'><b>*&nbsp;User ID:</b>&nbsp;<br>(to uniquely identify you on this site)</td><td><input type='text' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' name='userid' size='30' maxlength='100' value='""" + fieldsDict.get('userid', '') + """'></td></tr>
	<tr><td align='center'><b>*&nbsp;Password:</b></td><td><input type='password' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' name='passwd' size='30' maxlength='100' value='""" + fieldsDict.get('passwd', '') + """'></td></tr>
	<tr><td align='center'><b>*&nbsp;Retype&nbsp;Password:</b></td><td><input type='password' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' name='passwd2' size='30' maxlength='100' value='""" + fieldsDict.get('passwd2', '') + """'></td></tr>
	<tr><td align='center'><b>&nbsp;Email Address:</b></td><td><input type='text' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' name='emailid' size='30' maxlength='100' value='""" + fieldsDict.get('emailid', '') + """'></td></tr>
	<tr><td colspan='2' align='center'>&nbsp;</td></tr>
	<tr><td colspan='2' align='center'><input type='button' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;' name='btnRegister' value='Register' onClick='javascript:submitRegistration();'>&nbsp;&nbsp;&nbsp;<input type='button' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;' name='btnCancel' value='Cancel' onClick='javascript:cancelRegistration();'></td></tr>
	</table>
	</form>
	</center>
	</body></html>"""
    return(registrationForm)

def LoginForm(hostname = "localhost:8000", error_msg = "", fieldsDict = {}):
    loginForm = """<html><head>
      <title>SaveWhatYouLookedAt.com Account Login</title>
      <script language='JavaScript'>

	String.prototype.trim = function() {
	    a = this.replace(/^\s+/, '');
	    return a.replace(/\s+$/, '');
	};

	function submitCredentials(){
		if(validateInput()){
		    document.loginform.action = "http://""" + hostname + """/savewhatyoulookedat/login/";
		    document.loginform.submit();
		}
	}

	function validateInput(){
	    if(document.loginform.userid.value.trim() == ""){
		alert("Please enter your user ID");
		document.loginform.userid.value = "";
		document.loginform.userid.focus();
		return(false);
	    }
	    if(document.loginform.passwd.value.trim() == ""){
		alert("Please enter your password");
		document.loginform.passwd.value = ""
		document.loginform.passwd.focus();
		return(false);
	    }
	    return(true);
	}
	</script>
	<LINK href="css/forms.css" type=text/css rel=stylesheet>
	</head>
	<body bgcolor='#5588BB'>
	<center><font color='#FF0000'><b>""" + error_msg + """</b></font></center>
	<div class='alignleft'></div>
	<div class='alignright'></div>
	<center><form name='loginform' action='' method='POST'>
	<b>Enter User ID:</b>&nbsp;<input style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' type='text' name='userid' value='""" + fieldsDict.get('userid', '') + """'><br>
	<b>Enter Password:</b>&nbsp;<input style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;' type='password' name='passwd' value=''><br>
	<input style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;' type='button' name='btnsubmit' value='Login' onClick='javascript:submitCredentials();'>&nbsp;&nbsp;&nbsp;&nbsp;<input style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;' type='reset' name='reset1' value='Clear'>
	</form><br>New User? Click <a href='http://""" + hostname + """/savewhatyoulookedat/register/'>here</a> to register</center>
	</body></html>"""
    return(loginForm)

def RegistrationSuccessful(hostname = "localhost:8000", status_msg = ""):
    registeredSuccessfullyPage = """<html><head>
      <title>Congrats! You have successfully registered yourself...</title>
      </head>
      <body bgcolor='#5588BB'><br><br><br><br><br><br><br><br><center><font color='#0000FF'><b>""" + status_msg + """</b></font><br>
      Please click <a href='http://""" + hostname + """/savewhatyoulookedat/login/'><b><i><font color='#0000FF'>here</font></b></i></a> to login and continue.<br><br>Click <b><i><a href='#' onClick='javascript:self.close();'><font color='#0000FF'>here</font></a></i></b> to close this window and exit.
      </center>
      </body></html>"""
    return(registeredSuccessfullyPage)

def SaveURLForm(hostname = "localhost:8000", status_msg = "", fieldsDict = {}):
    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
    getcategorySQL = "select categoryID, categoryname from savewhatyoulookedat_category where userID='' or userID='" + fieldsDict.get('userid', '') + "'"
    sqlcursor = dbconn.cursor()
    sqlcursor.execute(getcategorySQL)
    cat_recs = sqlcursor.fetchall()
    CATEGORIES = {}
    for rec in cat_recs:
	CATEGORIES[rec[1]] = rec[0]
    saveUrlForm = """<html><head>
	<title>Save URLs - SaveWhatYouLookedAt.com</title>
      <script language='JavaScript'>
	
	var objhttp;
	var visitedURL;
	String.prototype.trim = function() {
	    a = this.replace(/^\s+/, '');
	    return a.replace(/\s+$/, '');
	};
	
	function getXMLHTTPObject(){
	    // Create XMLHttpRequest object
	    objhttp=(window.XMLHttpRequest)?new XMLHttpRequest():new ActiveXObject('Microsoft.XMLHTTP');
	    // Return if something crapped...
	    if(!objhttp){
		alert("Could nor create XMLHTTPRequest object.");
		return (0);
	    }
	    // ... but if it didn't, set callback and return object.
	    objhttp.onreadystatechange = getResponse;
	    return objhttp;
	}

	function initResponse(){
	    var ctr = 0;
	    for(ctr = 0; ctr < response.length; ctr++){
		response[ctr] = new String(""); // initialized to empty strings.
	    }
	}

	function getResponse(){
	    // Did we recieve the response?
	    if(objhttp.readyState == 4){
		responseFlag = 1;
		var status = objhttp.status;
		if(status == 200){
		    alert("URL " + visitedURL + " was successfully posted.");
		    self.close();
		}
		else{
		    alert("The URL " + visitedURL + " could not be posted. Please try again." + objhttp.responseText);
		}
	    }
	}

	function sendRequest(url,data,method,mode,header){
	    if(!mode){mode=true};
	    if(!header){
		header="Content-Type:application/x-www-form-urlencoded; charset=UTF-8";
	    }
	    //visitedURL = escape(data);
	    visitedURL = data;
	    objhttp=getXMLHTTPObject();
	    objhttp.open(method,url,mode);
	    objhttp.setRequestHeader(header.split(':')[0],header.split(':')[1]);
	    objhttp.send(visitedURL);
	    return (objhttp);
	}

	function validateInput(){
	    if(document.frmSaveURL.userid.value.trim() == "" || document.frmSaveURL.sessid.value.trim() == ""){
		alert("You have to be logged in to be able to post your URL data");
		window.location.href = "http://""" + hostname + """/savewhatyoulookedat/login/";
		return(false);
	    }
	    if(document.frmSaveURL.vURL.value.trim() == ""){
		alert("You do not have an URL to save. Please copy-paste the URL you wish to save in the box labelled URL and try to save.");
		document.frmSaveURL.vURL.value = "";
		document.frmSaveURL.vURL.focus();
		return(false);
	    }
	    if(document.frmSaveURL.bookmark.value.trim() == ""){
		alert("Please enter a name for the URL");
		document.frmSaveURL.bookmark.value = "";
		document.frmSaveURL.bookmark.focus();
		return(false);
	    }
	    var catSelected = "False";
	    for(var i=0; i < document.frmSaveURL.category.options.length; i++){
		if(document.frmSaveURL.category.options[i].selected == true){
		    catSelected = true;
		    break;
		}
	    }
	    if(catSelected == true){
		return(true);
	    }
	    else{
		return(false);
	    }
	}

	function saveUrl(userid, sessionid){
	    if(validateInput()){
		var postdatastr = "";
		postdatastr = postdatastr + "vURL=" +  document.frmSaveURL.vURL.value.trim() + "&userid=" + document.frmSaveURL.userid.value + "&sessid=" + document.frmSaveURL.sessid.value + "&bookmark=" + document.frmSaveURL.bookmark.value.trim() + "&category=" + document.frmSaveURL.category.options[document.frmSaveURL.category.options.selectedIndex].value + "&commandName=" + document.frmSaveURL.commandName.value + "&commandArgs=" + document.frmSaveURL.commandArgs.value;
		var targetURL = "http://""" + hostname + """/savewhatyoulookedat/";
		var method = "POST";
		//alert(document.frmSaveURL.vURL.value.trim());
		sendRequest(targetURL, postdatastr, method);
	    }
	}
	</script>
	</head>
	<STYLE type=text/css>
	      BODY {
		MARGIN: 26px 0px; BACKGROUND-COLOR: #f2f2f2
	      }
	</STYLE>
	<LINK href="css/main.css" type=text/css rel=stylesheet><!-- InstanceBeginEditable name="head" --><!-- InstanceEndEditable -->
	<LINK href="css/forms.css" type=text/css rel=stylesheet>
	<body bgcolor='#5588BB'>
	<center><font color='#FF0000'><b>""" + status_msg + """</b></font></center>
	<div class='alignleft'></div>
	<div class='alignright'></div>
	<center><form name='frmSaveURL' action='' method='POST'>"""
    urlVal = fieldsDict.get('vURL', '')
    bmarkVal = ""
    categoryVal = ""
    recvInfo = ""
    cmdName = fieldsDict.get('commandName', '')
    cmdArgs = fieldsDict.get('commandArgs', '')
    if cmdName == "edit":
	saveUrlForm += """<input type='hidden' name='commandName' value='save'><input type='hidden' name='commandArgs' value='""" + cmdArgs + """'>"""
	editRecordSQL = "select u.savedURL, c.categoryname, u.bookmark, u.recieveinfo from savewhatyoulookedat_urls u, savewhatyoulookedat_category c where u.urlID='" + cmdArgs + "' and c.categoryID = u.categoryID"
	sqlcursor.execute(editRecordSQL)
	urlrecs = sqlcursor.fetchall()
	for rec in urlrecs:
	    urlVal = rec[0]
	    categoryVal = rec[1]
	    bmarkVal = rec[2]
	    recvInfo = rec[3]
    else:
	saveUrlForm += """<input type='hidden' name='commandName' value='""" + cmdName + """'><input type='hidden' name='commandArgs' value='""" + cmdArgs + """'>"""
    saveUrlForm += """<table border=0 cellspacing=4 cellpadding=4><tr><td align=center><b>URL:</b>&nbsp;</td><td align='left'><input type='text' name='vURL' value='""" + urlVal + """' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;'></td></tr>
	<tr><td align='center'><b>Bookmark:</b></td><td align='left'>&nbsp;<input type='text' name='bookmark' value='""" + bmarkVal + """' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;'></td></tr><tr><td align='center'>
	<b>Category:</b>&nbsp;</td><td align='left'><select name='category' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px;'>"""
    for catname in CATEGORIES.keys():
	if catname == categoryVal:
	    saveUrlForm += """<option value='""" + CATEGORIES[catname].__str__() + """' selected>""" + catname + """</option>"""
	else:
	    saveUrlForm += """<option value='""" + CATEGORIES[catname].__str__() + """'>""" + catname + """</option>"""
    saveUrlForm += """</select></td></tr><tr><td align='center'>
	<input type='hidden' name='userid' value='""" + fieldsDict.get('userid', '') + """'></td><td>
	<input type='hidden' name='sessid' value='""" + fieldsDict.get('sessid', '') + """'></td></tr>
	<tr><td align='center' colspan=2><input type='button' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;' name='btnsubmit' value='Save' onClick="javascript:saveUrl('""" + fieldsDict.get('userid', '') + """', '""" + fieldsDict.get('sessid', '') + """');">&nbsp;&nbsp;&nbsp;&nbsp;<input type='button' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;' name='btnClose' value='Close' onClick='javascript:self.close();'></td></tr></table>
	</form></center>
	</body></html>"""
    saveUrlForm += LandingPage(fieldsDict.get('userid', ''), fieldsDict.get('sessid', ''))
    return(saveUrlForm)

def LandingPage(userid, sessid, status_msg = "", fieldsDict = {}):
    html = """<html><head>
	<title>Save URLs - SaveWhatYouLookedAt.com</title>
	<Script Language='JavaScript'>
	   
	    function downloadFfPlugin(){
		window.location.href = '/savewhatyoulookedat/downloadPlugin/?user_id="""
    html += userid + """&session_id=""" + sessid
    html += """';
		return(true);
	    }

	    function manageData(user, session){
		var manageDataURL = "/savewhatyoulookedat/managedata/?session=" + session + "&user=" + user;
		mWin = window.open(manageDataURL, "managedatawin", "width=600,height=450,resizable=false,location=no,status=no,scrollbars=yes,menubar=no,toolbar=no");
		return (true);
	    }
	    var logouthttp;
	    function doLogout(userid, sessid){
		if(userid.length == 0 && sessid.length == 0){
		    return; // No need of making a POST request as there is no existing session.
		}
		logouthttp=(window.XMLHttpRequest)?new XMLHttpRequest():new ActiveXObject('Microsoft.XMLHTTP');
		var logoutData = "userid=" + userid + "&sessid=" + sessid;
		header="Content-Type:application/x-www-form-urlencoded; charset=UTF-8";
		var logoutURL = "/savewhatyoulookedat/logout/";
		// Return if something crapped...
		if(!logouthttp){
		    alert("Could nor create XMLHTTPRequest object.");
		    return (0);
		}
		// ... but if it didn't, set callback and return object.
		logouthttp.onreadystatechange = showMessage;
		logouthttp.open('POST',logoutURL, true);
		logouthttp.setRequestHeader(header.split(':')[0],header.split(':')[1]);
		logouthttp.send(logoutData);
	    }
 
	    function showMessage(){
		if(logouthttp.readyState == 4){
		    var status = logouthttp.status;
		    if(status == 200){
			logoutResponse = logouthttp.responseText;
			alert(logoutResponse);
			window.location.href = "/savewhatyoulookedat/login/";
		    }
		    else{
			alert("The server could not be contacted. " + logoutResponse);
		    }
		}
	    }

	    function launchSearchWindow(userid, sessid){
		var searchURL = 'http://""" + WEB_HOST + """/savewhatyoulookedat/search/?userid=' + userid + '&sessid=' + sessid;
		var searchWin = window.open(searchURL, "searchURLWin", "width=850,height=450,resizable=false,location=no,status=no,scrollbars=yes,menubar=no,toolbar=no");
	    }
	</Script>
	<STYLE type=text/css>
	      BODY {
		MARGIN: 26px 0px; BACKGROUND-COLOR: #f2f2f2
	      }
	</STYLE>
	<LINK href="css/main.css" type=text/css rel=stylesheet><!-- InstanceBeginEditable name="head" --><!-- InstanceEndEditable -->
	</head>
	<body>
	<center>
	<b><i>""" + status_msg + """</i></b><br>
	<table style="BACKGROUND-COLOR: #ffffff"><tr><td class=topmenu><a href='/savewhatyoulookedat/login/'  class=topmenu>Login Page</a></td><td class=topmenu><a href='/savewhatyoulookedat/register/' class=topmenu>Register here</a></td><td class=topmenu><a href='#' onClick='javascript:downloadFfPlugin();' class=topmenu>Download Firefox Plugin</a></td><td class=topmenu><a href='/savewhatyoulookedat/?userid=""" + userid + """&sessid=""" + sessid + """'>Save URL</a></td>"""
    if userid.__len__() > 0 and sessid.__len__() > 0:
	dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
	chkCursor = dbconn.cursor()
	chkSQL = "select sessionState from savewhatyoulookedat_session where sessionID='" + sessid + "' and user_id='" + userid + "'"
	chkCursor.execute(chkSQL)
	chkRecs = chkCursor.fetchall()
	if chkRecs[0][0] == 1:
	    html += """<td class=topmenu><a href='#' onClick="javascript:manageData('""" + userid + """', '""" + sessid + """');" class=topmenu>Manage URLs</a></td><td class=topmenu><a href='#' onClick="javascript:launchSearchWindow('""" + userid + """', '""" + sessid + """');">Search URL</a></td><td class=topmenu><a href='#' onClick="javascript:doLogout('""" + userid + """', '""" + sessid + """');" class=topmenu>Logout</a></td></tr>"""
    html += """</table></center>
	</body></html>"""
    return(html)

def manageDataFormHeader(userid, sessid, status_msg = "", fieldsDict = {}):
    headerHTML = """<html><head>
	<title>SaveWhatYouLookedAt.com - Manage URLs and Data</title>"""
    jsContent = manageFormJavascript(userid, sessid)
    headerHTML += jsContent + """<STYLE type=text/css>
	      BODY {
		MARGIN: 26px 0px; BACKGROUND-COLOR: #f2f2f2
	      }
	</STYLE>
	<LINK href="css/main.css" type=text/css rel=stylesheet><!-- InstanceBeginEditable name="head" --><!-- InstanceEndEditable -->
	</head>
	<body bgcolor='#5588BB'>
	<center><font color='#0000FF'><b>""" + status_msg + """</b></font></center>
	<p>
	<center><h3>Manage URLs and Associated Data</h3><br></center>
	<p>
	<center>
	<form name='frmManageURLs' method='POST' action='/savewhatyoulookedat/managedata/'>
	<input type='hidden' name='user' value='""" + userid + """'><input type='hidden' name='session' value='""" + sessid + """'><input type='hidden' name='commandName' value=''><input type='hidden' name='commandArgs' value=''>
	<table style="BACKGROUND-COLOR: #cdddf7" border='0' width='80%' cellspacing='2' cellpadding='2'> """
    return(headerHTML)

def manageDataFormFooter(userid, sessid, status_msg = "", fieldsDict = {}):
    footerHTML = """<tr><td colspan='9' align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px"><input type='button' name='btnAddCategory' value='Add Category' onClick="javascript:addCategory();">&nbsp;&nbsp;<input type='button' name='btnDeleteSelected' value='Delete Selected' onClick="javascript:deleteSelected();">&nbsp;&nbsp;<input type='button' name='btnRefreshPage' value='Refresh Page' onClick="javascript:refreshPage();">&nbsp;&nbsp;<input type='button' name='btnCloseWindow' value='Close Window' onClick="javascript:closeWindow();"></td></tr>"""
    footerHTML += """</table></form></center>"""
    footerHTML += """<br></body></html>"""
    return(footerHTML)

def manageDataTableHeader(userid, sessid, status_msg = "", fieldsDict = {}):
    tableHeaderHTML = """<tr><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'><input type='checkbox' name='chkAll' value='all' onClick='javascript:selectAllRecords();'></font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'>URL</font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'>Category</font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'>Bookmark</font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'>Page&nbsp;Content</font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'>Page&nbsp;Images</font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'>Email&nbsp;Addresses</font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'> Last&nbsp;&nbsp;Accessed</font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'>Update&nbsp;Setting</font></b></td><td align='center' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b><font color='#0000FF'>&nbsp;&nbsp;&nbsp;&nbsp;Edit/Delete&nbsp;&nbsp;&nbsp;&nbsp;</font></b></td></tr>"""
    return(tableHeaderHTML)

def manageDataTableRow(userid, sessid, status_msg = "", fieldsDict = {}):
    tableRowHTML = """<tr><td align='right' class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'><input type='checkbox' name='chkRecord' value='%s'>&nbsp;%s</font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'>%s</font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'>%s</font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'>%s</font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'><a href='#' onClick="javascript:showPageHTMLContent('%s');">%s</a></font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'>%s</font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'>%s</font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'>%s</font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'>%s</font></td><td class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><font color='#0000FF'><input type='button' name='btnEdit' value='Edit' onClick="javascript:editRecord('%s');">&nbsp;<input type='button' name='btnDelete' value='Delete' onClick="javascript:deleteRecord('%s');"></font></td></tr>"""
    return(tableRowHTML)

def manageFormJavascript(userid, sessid):
    javascript = """<script Language='JavaScript'>

	String.prototype.trim = function() {
	    a = this.replace(/^\s+/, '');
	    return a.replace(/\s+$/, '');
	};
	
	function editRecord(url_id){
	    var newwin = window.open("", "editwin", "width=400,height=400,resizable=false,location=no,status=no,scrollbars=yes,menubar=no,toolbar=no");
	    document.frmManageURLs.commandName.value = "edit";
	    document.frmManageURLs.commandArgs.value = url_id;
	    document.frmManageURLs.action = "/savewhatyoulookedat/?userid=""" + userid + """&sessid=""" + sessid + """";
	    document.frmManageURLs.method="POST";
	    document.frmManageURLs.target = "editwin";
	    document.frmManageURLs.submit();
	    return(true);
	}

	function deleteRecord(url_id){
	    var confirmMessage = "Performing this action will permanently remove the selected record(s) from the database.Are you sure you wish to continue?";
	    if(confirm(confirmMessage)){
		document.frmManageURLs.commandName.value = "delete";
		document.frmManageURLs.commandArgs.value = url_id;
		document.frmManageURLs.action = "/savewhatyoulookedat/commandHandler/";
		document.frmManageURLs.method="POST";
		document.frmManageURLs.submit();
		return(true);
	    }
	    return(false);
	}

	function addCategory(){
	    var customcat = prompt("Enter a name for your custom category", "");
	    if(customcat.trim() == ""){
		alert("The name you entered is invalid. Your custom category name should contain atleast 1 alphanumeric character");
		return(false);
	    }
	    document.frmManageURLs.commandName.value = "addcat";
	    document.frmManageURLs.commandArgs.value = customcat;
	    document.frmManageURLs.action = "/savewhatyoulookedat/commandHandler/";
	    document.frmManageURLs.method="POST";
	    document.frmManageURLs.submit();
	    return(true);
	}

	function deleteSelected(){
	    var validityMessage = "You haven't selected any record. Select one or more records and try again.";
	    var countChecked = 0;
	    for(var i=0;i < document.frmManageURLs.chkRecord.length; i++){
		if(document.frmManageURLs.chkRecord[i].checked){
		    countChecked++;
		}
	    }
	    if(countChecked == 0){
		alert(validityMessage);
		return(false);
	    }
	    var confirmMessage = "Performing this action will permanently remove the selected record(s) from the database.Are you sure you wish to continue?";
	    if(confirm(confirmMessage)){
		document.frmManageURLs.commandName.value = "delete";
		var url_id_list_str = "";
		for(var i=0;i < document.frmManageURLs.chkRecord.length; i++){
		    if(document.frmManageURLs.chkRecord[i].checked){
			url_id_list_str = url_id_list_str + document.frmManageURLs.chkRecord[i].value + ",";
		    }
		}
		url_id_list_str = url_id_list_str.substring(0, url_id_list_str.length - 1);
		//alert(url_id_list_str);
		document.frmManageURLs.commandArgs.value = url_id_list_str;
		document.frmManageURLs.action = "/savewhatyoulookedat/commandHandler/";
		document.frmManageURLs.method="POST";
		document.frmManageURLs.submit();
		return(true);
	    }
	    return(false);
	}

	function refreshPage(){
	    window.location.reload(true);
	}

	function closeWindow(){
	    window.close();
	}

	function selectAllRecords(){
	    for(var i=0; i < document.frmManageURLs.chkRecord.length; i++){
		document.frmManageURLs.chkRecord[i].checked = document.frmManageURLs.chkAll.checked;
	    }
	}

	function showPageHTMLContent(html){
	    var htmlwin = window.open("", "html", "width=400,height=400,resizable=false,location=no,status=no,scrollbars=yes,menubar=no,toolbar=no");
	    htmlwin.document.write("<center>" + html + "</center>");
	    return(true);
	}

	function showImage(imgpath, userid, sessid){
	    var imgwin = window.open("/savewhatyoulookedat/showimage/?imgp=" + imgpath + "&userid=" + userid + "&sessid=" + sessid, "img", "width=400,height=400,resizable=false,location=no,status=no,scrollbars=yes,menubar=no,toolbar=no");
	    return(true);
	}

	</script>"""
    return(javascript)


def getSearchHeader(userid, sessid, searchParams={}):
    searchTitle = "Search Form"
    searchKeys = searchParams.keys()
    if searchKeys.__len__() > 0:
	searchTitle = "Search Results"
    headerHTML = """<html>
	<head>
	<title>%s</title>"""%(searchTitle)
    headerHTML += manageFormJavascript(userid, sessid)
    headerHTML += """<script language="javascript">
	    // Javascript Search UI related functions:
	    function submitSearch(){
		if(document.frmSearch.searchBookmark.value.trim() == "" && document.frmSearch.searchURL.value.trim() == "" && document.frmSearch.searchCategory.value == "" && document.frmSearch.searchContent.value.trim() == "" && document.frmSearch.searchDate.value == ""){
		    alert("You have not specified any parameter for search! Please set one or more parameters and try again.");
		    document.frmSearch.searchBookmark.focus();
		    return(false);
		}
		else{
		    document.frmSearch.searchBookmark.value = document.frmSearch.searchBookmark.value.trim();
		    document.frmSearch.searchURL.value = document.frmSearch.searchURL.value.trim();
		    document.frmSearch.searchContent.value = document.frmSearch.searchContent.value.trim();
		    document.frmSearch.submit();
		    return(true);
		}
	    }

	    function showRecordDetails(urlid, url, bookmark, title, category, accesstime, emailids, recieveinfo){
		recieveinfo_text = "Enabled";
		if(recieveinfo == 0){
		    recieveinfo_text = "Disabled";
		}
		if(emailids.trim() == ""){
		    emailids = "None";
		}
		var detwin = window.open("", 'detailswin', "width=400,height=400,resizable=false,location=no,status=no,scrollbars=yes,menubar=no,toolbar=no");
		detwin.document.open("text/html");
		detwin.document.write("<html><head><title>Record Details</title></head><body bgcolor='#cdddf7'>");
		detwin.document.write("<center><table border='0' cellspacing='2' cellpadding='2'>");
		detwin.document.write("<tr><td><b><font color='#0000FF'>URL ID:</b>&nbsp;&nbsp;</font></td><td><font color='#0000FF'>" + urlid + "</font></td></tr>");
		detwin.document.write("<tr><td><b><font color='#0000FF'>URL:</b>&nbsp;&nbsp;&nbsp;&nbsp;</font></td><td><font color='#0000FF'>" + url + "</font></td></tr>");
		detwin.document.write("<tr><td><b><font color='#0000FF'>Title:</b>&nbsp;&nbsp;&nbsp;</font></td><td><font color='#0000FF'>" + title + "</font></td></tr>");
		detwin.document.write("<tr><td><b><font color='#0000FF'>Category:</b>&nbsp;</font></td><td><font color='#0000FF'>" + category + "</font></td></tr>");
		detwin.document.write("<tr><td><b><font color='#0000FF'>Access Date/Time:</b>&nbsp;&nbsp;&nbsp;</font></td><td><font color='#0000FF'>" + accesstime + "</font></td></tr>");
		detwin.document.write("<tr><td><b><font color='#0000FF'>Email ID:</b>&nbsp;</font></td><td><font color='#0000FF'>" + emailids + "</font></td></tr>");
		detwin.document.write("<tr><td><b><font color='#0000FF'>Recieve Info:</b>&nbsp;</font></td><td><font color='#0000FF'>" + recieveinfo_text + "</font></td></tr>");
		detwin.document.write("<tr><td colspan='2' align='center'><b><font color='#0000FF'><input type='button' name='btnClose' value='Close' onClick='javascript:self.close();'></font></td></tr>");
		detwin.document.write("</table></center>");
		detwin.document.write("</body></html>");
		detwin.document.close();
	    }
	</script>
	<STYLE type=text/css>
	      BODY {
		MARGIN: 26px 0px; BACKGROUND-COLOR: #f2f2f2
	      }
	</STYLE>
	<LINK href="css/main.css" type=text/css rel=stylesheet><!-- InstanceBeginEditable name="head" --><!-- InstanceEndEditable -->
	<LINK href="css/forms.css" type=text/css rel=stylesheet>
	</head>
	<body bgcolor='#5588BB'>"""
    return(headerHTML)

def getSearchForm(userid, sessid, searchParams={}):
    formTitle = "Search Form"
    searchBookmark = ""
    searchURL = ""
    searchCategory = ""
    searchContent = ""
    searchDate = ""
    categories = [ "<option value=''>Select Category</option>" ]
    accessDates = [ "<option value=''>Select Access Date</option>" ]
    BookmarkLogicURL = "OR" # All logic operations are set to "OR" by default in order to maximize the search resultset.
    URLLogicCategory = "OR"
    CategoryLogicContent = "OR"
    ContentLogicDate = "OR"
    if searchParams.has_key("searchBookmark"):
	searchBookmark = searchParams["searchBookmark"]
    if searchParams.has_key("searchURL"):
	searchURL = searchParams["searchURL"]
    if searchParams.has_key("searchCategory"):
	searchCategory = searchParams["searchCategory"]
    if searchParams.has_key("searchContent"):
	searchContent = searchParams["searchContent"]
    if searchParams.has_key("searchDate"):
	searchDate = searchParams["searchDate"]
    if searchParams.has_key("BookmarkLogicURL"):
	BookmarkLogicURL = searchParams["BookmarkLogicURL"]
    if searchParams.has_key("URLLogicCategory"):
	URLLogicCategory = searchParams["URLLogicCategory"]
    if searchParams.has_key("CategoryLogicContent"):
	CategoryLogicContent = searchParams["CategoryLogicContent"]
    if searchParams.has_key("ContentLogicDate"):
	ContentLogicDate = searchParams["ContentLogicDate"]
    bookmarkUrlLogicOptions = "<option value='OR' selected>&nbsp;&nbsp;OR&nbsp;&nbsp;</option>\n<option value='AND'>&nbsp;AND&nbsp;</option>"
    urlCategoryLogicOptions = "<option value='OR' selected>&nbsp;&nbsp;OR&nbsp;&nbsp;</option>\n<option value='AND'>&nbsp;AND&nbsp;</option>"
    categoryContentLogicOptions = "<option value='OR' selected>&nbsp;&nbsp;OR&nbsp;&nbsp;</option>\n<option value='AND'>&nbsp;AND&nbsp;</option>"
    contentDateLogicOptions = "<option value='OR' selected>&nbsp;&nbsp;OR&nbsp;&nbsp;</option>\n<option value='AND'>&nbsp;AND&nbsp;</option>"
    if BookmarkLogicURL == "AND":
	bookmarkUrlLogicOptions = "<option value='OR'>&nbsp;&nbsp;OR&nbsp;&nbsp;</option>\n<option value='AND' selected>&nbsp;AND&nbsp;</option>"
    if URLLogicCategory == "AND":
	urlCategoryLogicOptions = "<option value='OR'>&nbsp;&nbsp;OR&nbsp;&nbsp;</option>\n<option value='AND' selected>&nbsp;AND&nbsp;</option>"
    if CategoryLogicContent == "AND":
	categoryContentLogicOptions = "<option value='OR'>&nbsp;&nbsp;OR&nbsp;&nbsp;</option>\n<option value='AND' selected>&nbsp;AND&nbsp;</option>"
    if ContentLogicDate == "AND":
	contentDateLogicOptions = "<option value='OR'>&nbsp;&nbsp;OR&nbsp;&nbsp;</option>\n<option value='AND' selected>&nbsp;AND&nbsp;</option>"
    dbconn = MySQLdb.connect(DB_HOST, DB_USERID, DB_PASSWD, DB_SCHEMA_NAME)
    dbCursor = dbconn.cursor()
    categoriesSQL = "select categoryname from savewhatyoulookedat_category where userID='" + userid + "' or userID=''"
    accessDateSQL = "select startTime from savewhatyoulookedat_session where user_id='" + userid + "'"
    dbCursor.execute(categoriesSQL)
    catRecs = dbCursor.fetchall()
    for cat in catRecs:
	if cat[0] == searchCategory:
	    categories.append("<option value='" + cat[0] + "' selected>" + cat[0] + "</option>")
	else:
	    categories.append("<option value='" + cat[0] + "'>" + cat[0] + "</option>")
    dbCursor.execute(accessDateSQL)
    adateRecs = dbCursor.fetchall()
    uniqueDates = {}
    for accessDate in adateRecs:
	datepart, timepart = accessDate[0].__str__().split(" ")
	if uniqueDates.has_key(datepart):
	    continue
	uniqueDates[datepart] = datepart
	if datepart == searchDate:
	    accessDates.append("<option value='" + datepart.__str__() + "' selected>" + datepart.__str__() + "</option>")
	else:
	    accessDates.append("<option value='" + datepart.__str__() + "'>" + datepart.__str__() + "</option>")
    categoryOptionsString = "\n".join(categories)
    accessDatesOptionsString = "\n".join(accessDates)
    searchForm = """<br><center><h3><font color='#0000FF'>%s</font></h3></center><br>
	<center><form name='frmSearch' method='POST' action='/savewhatyoulookedat/search/'>
	<input type='hidden' name='userid' value='%s'><input type='hidden' name='sessid' value='%s'>
	<table width='90&perc;' cellspacing='2' cellpadding='2' border='0'>
	<tr><td colspan='3' align='center'><b><i>Search using one or more of the following parameters</i></b></td></tr>
	<tr><td width='20&perc;'><b>By Bookmark:&nbsp;</b></td><td width='75&perc;'><input type='text' name='searchBookmark' value='%s' size='70' maxlength='400' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'></td><td>&nbsp;<select name='BookmarkLogicURL' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'>%s</select>&nbsp;</td></tr>
	<tr><td width='20&perc;'><b>By URL:&nbsp;</b></td><td width='75&perc;'><input type='text' name='searchURL' value='%s' size='70' maxlength='400' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'></td><td>&nbsp;<select name='URLLogicCategory' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'>%s</select>&nbsp;</td></tr>
	<tr><td width='20&perc;'><b>By Category:&nbsp;</b></td><td width='75&perc;'><select name='searchCategory' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'>%s</select></td><td>&nbsp;<select name='CategoryLogicContent' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'>%s</select>&nbsp;</td></tr>
	<tr><td width='20&perc;'><b>By Content:&nbsp;</b></td><td width='75&perc;'><input type='text' name='searchContent' value='%s' size='70' maxlength='400' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'></td><td>&nbsp;<select name='ContentLogicDate' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'>%s</select>&nbsp;</td></tr>
	<tr><td width='20&perc;'><b>By Access Date:&nbsp;</b></td><td width='75&perc;'><select name='searchDate' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;'>%s</select></td><td>&nbsp;</td></tr>
	<tr><td colspan='3' align='center'><input type='button' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;' name='btnSearch' value='Search' onClick="javascript:submitSearch();">&nbsp;&nbsp;&nbsp;&nbsp;<input type='button' style='border: 1px solid rgb(204, 204, 204); margin: 0pt 0pt 5px; background: rgb(221, 221, 221) none repeat scroll 0% 0%; -moz-border-radius-topleft: 5px; -moz-border-radius-topright: 5px; -moz-border-radius-bottomright: 5px; -moz-border-radius-bottomleft: 5px; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;' name='btnClose' value='Close' onClick="javascript: self.close();"></td></tr>
	</table>
	</form>
	<br><hr>
    <br>"""%(formTitle, userid, sessid, searchBookmark, bookmarkUrlLogicOptions, searchURL, urlCategoryLogicOptions, categoryOptionsString, categoryContentLogicOptions, searchContent, contentDateLogicOptions, accessDatesOptionsString)
    return(searchForm)

def searchResultsBody(userid, sessid, searchResults=[]):
    searchTitle = "<font color='#0000FF'>"
    if searchResults.__len__() == 1:
	searchTitle += "<h3>Search - " + searchResults.__len__().__str__() + " match found</h3></font>"
    elif searchResults.__len__() > 1:
	searchTitle += "<h3>Search - " + searchResults.__len__().__str__() + " matches found</h3></font>"
    else:
	searchTitle += "<h3>Search - No match found</h3></font>"
    resultBodyHTML = """<br><center>%s</center><br><br>
	<center><table width='90&perc;' cellspacing='2' cellpadding='2' style="BACKGROUND-COLOR: #cdddf7">
	    <tr><td width='5&perc;' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b>Serial #</b></td><td width='25&perc;' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b>URL</b></td><td width='20&perc;' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b>Bookmark</b></td><td width='30&perc;' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b>Page Title</b></td><td width='10&perc;' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b>Access Time</b></td><td width='10&perc;' style="PADDING-RIGHT: 14px; PADDING-LEFT: 13px;BACKGROUND-COLOR: #aaccff"><b>Category</b></td></tr>"""%(searchTitle)
    ctr = 1
    for searchrec in searchResults:
	searchRow = """<tr><td width='5&perc;' class=tabletextbold1 style="BACKGROUND-COLOR: #87deff">%s</td><td width='25&perc;' class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><a href='%s' target=_blank>%s</a></td><td width='20&perc;' class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><a href='#' onClick="javascript:showRecordDetails('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');">%s</a></td><td width='30&perc;' class=tabletextbold1 style="BACKGROUND-COLOR: #87deff"><a href='#' onClick="javascript:showPageHTMLContent('%s');" alt='click here to see the cached contents of the page'>%s</a></td><td width='10&perc;' class=tabletextbold1 style="BACKGROUND-COLOR: #87deff">%s</td><td width='10&perc;' class=tabletextbold1 style="BACKGROUND-COLOR: #87deff">%s</td></tr>"""%(ctr.__str__(), searchrec["savedURL"], searchrec["savedURL"], searchrec["urlID"], searchrec["savedURL"], searchrec["bookmark"], searchrec["title"],  searchrec["categoryName"], searchrec["accesstime"], searchrec["emailID_list"], searchrec["recieveinfo"], searchrec["bookmark"], searchrec["html"], searchrec["title"] + " ...[more]", searchrec["accesstime"], searchrec["categoryName"])
	ctr += 1
	resultBodyHTML += searchRow
    resultBodyHTML += """</table></center>"""    
    return(resultBodyHTML)

def getSearchFooter():
    footerHTML = """<br><br></body></html>"""
    return(footerHTML)
