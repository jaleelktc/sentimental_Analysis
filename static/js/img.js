

function localFilename(url)	// creating a counter file
{
	var x = url.lastIndexOf("/");
	url = url.slice(x + 1);
	return url;		
}


function changeImage(element)
{ 
	var v = element.getAttribute("src");
	v = localFilename(v);   // for a local filename

	if(v == "feed-blue.png")
		v = "feed-orange.png";
	else
		v = "feed-blue.png";

	element.setAttribute("src", v);	

}

function changeBackground()
{
	var z = new Image();
	z.src = "http://www.xul.fr/images/road.jpg";
	document.body.background=z.src;
} 


