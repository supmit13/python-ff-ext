    function getXMLHTTPObject(){
		//instantiate new XMLHttpRequest object
		var objhttp=(window.XMLHttpRequest)?new XMLHttpRequest():new ActiveXObject('Microsoft.XMLHTTP');
		if(!objhttp){return};
		// assign event handler
		objhttp.onreadystatechange=displayStatus;
		// return XMLHttpRequest object
		return objhttp;
    }

    function sendRequest(url,data,method,mode,header){
		// set default values
		if(!url){url='default_url.htm'};
		if(!data){data='defaultdata=defaultvalue'};
		if(!method){method='post'};
		if(!mode){mode=true};
		if(!header){header='Content-Type:application/x-www-form-urlencoded; charset=UTF-8'};
		// get XMLHttpRequest object
		objhttp=getXMLHTTPObject();
		// open socket connection
		objhttp.open(method,url,mode);
		// set http header
		objhttp.setRequestHeader(header.split(':')[0],header.split(':')[1]);
		// send data
		objhttp.send(data);
    }

    function displayStatus(){
		// check XMLHttpRequest object status
		if(objhttp.readyState==4){
			// create paragraph elements
			var parStat=document.createElement('p');
			var parText=document.createElement('p');
			var parResp=document.createElement('p');
			// assign ID attributes
			parStat.id='status';
			parText.id='text';
			parResp.id='response';
			// append text nodes
			parStat.appendChild(document.createTextNode('Status : '+objhttp.status));
			parText.appendChild(document.createTextNode('Status text : '+objhttp.statusText));
			parResp.appendChild(document.createTextNode('Document code : '+objhttp.responseText));
			// insert <p> elements into document tree
			document.body.appendChild(parStat);
			document.body.appendChild(parText);
			document.body.appendChild(parResp);
		}
    }    


	
	var url = 'http://192.168.228.129/cgi-bin/pystat/graphPage.py';
	var data = 'dataset_type=both&datasets=both&genFlag=1&granularity=cumulative&productID=-1&productID=10002&productID=10003&productID=10004&productID=10009&productID=10010&productID=10011&productID=10012&range_baseline=1990Jan&range_baseline=1990Feb&range_baseline=1990Mar&range_baseline=1990Apr&range_baseline=1990May&range_baseline=1990Jun&range_baseline=1990Jul&range_baseline=1990Aug&range_baseline=1990Sep&range_baseline=1990Oct&range_baseline=1990Nov&range_baseline=1990Dec&range_baseline=1991Jan&range_baseline=1991Feb&range_end=1996Apr&range_recent=1995Jan&range_recent=1995Feb&range_recent=1995Mar&range_recent=1995Apr&range_recent=1995May&range_recent=1995Jun&range_recent=1995Jul&range_recent=1995Aug&range_recent=1995Sep&range_recent=1995Oct&range_recent=1995Nov&range_recent=1995Dec&range_recent=1996Jan&range_recent=1996Feb&range_recent=1996Mar&range_recent=1996Apr&range_start=1995Jan&reportName=juymediancum&statOperations=Median&storeID=-1&storeID=157&xaxisunit=product&zeros=exczeros';
	var method = 'post';
	sendRequest(url, data, method);




