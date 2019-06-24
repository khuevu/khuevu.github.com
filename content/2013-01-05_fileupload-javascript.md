Title: Uploading file using Javascript
Category: Technology
Tags: javascript, facebook graph

A few months ago, I have written a [chrome extension](https://chrome.google.com/webstore/detail/social-snap/bnhlaifngpmodnnkpebagndhomlcnaed) for instant sharing of captured content of a webpage to Facebook. So one of the requirement is that the captured image data is uploaded to Facebook. The familiar web flow of uploading a file to serverwould be presenting user with upload file form (html form with enctype="multipart/form-data") and let them select the file: 

    #!html
    <form action="https://graph.facebook.com/me/photos?access_token=..." method="post"
    enctype="multipart/form-data">
    <label for="file">Filename:</label>
    <input type="file" name="file" id="file"><br>
    <input type="submit" name="submit" value="Submit">
    </form>

So how do we accomplish it in Javascript? First, we need to know what is actually sent in the body of the HTTP request when a file is uploaded using the above method. Well, the body of request originated from a "multiplart/form-data" form is indeed a multipart message. The message follows the [MIME internet standard](http://en.wikipedia.org/wiki/MIME).  
## MIME standard

MIME was intended to be the standard for describing content of an email. An email messages often consists of multiple part, for example, text, non-ASCII language content, attachement, binary content (images, movies). Its usage, however, have extended far beyond the field of email. 

HTTP uses MIME standard when it needs to transfer data which is binary or and may mix with other data format. One essential thing to know about MIME is that its initial design requirements include requiring no changes to existing email servers, which only support plain text email. Thus you will be right if you expect the MIME message to be sent as plain text message (ASCII characters). The HTTP file upload request we will examine is also in the plain text format like usual HTTP POST requests. 

## HTTP multipart request:

When uploading a photo to facebook, open firebug and observe the request:

    Content-Type: multipart/form-data; boundary=boundary

    #!http
    --boundary
    Content-Disposition: form-data; name="source"; filename="capture.png"
    Content-Type: image/png

    PGh0bWw+CiAgPGhlYWQ+CiAgPC9oZWFkPgogIDxib2R5PgogICAgPHA+VGhpcyBpcyB0aGUg
     Ym9keSBvZiB0aGUgbWVzc2FnZS48L3A+CiAgPC9ib2R5Pgo8
    ... 
     L2h0bWw+Cg==
    --boundary
    Content-Disposition: form-data; name="message"

    My comment for the uploaded image
    --boundary--


We can observe from the message.

*   First the HTTP Request header. `Content-Type` attribute tell you that the message is a multipart message. Notice the `boundary` name value pair. It specifies the string that will be used as the message's parts separator. The boundary value can be any string which must not be contain in any other part of the message. It, appended with a `--` prefix, is used as boundary between parts. And it is appended `--` at both end to mark the end of the message.  
*   Each message part has its own headers. `Content-Type` is `image/png` for the image data. For the comment data, you can leave this header out as it is default to text. `Content-Disposition` in MIME standard supposes to tell the receiver how the content should be presented. In HTTP, it is used as request parameter's name. 
*   The request header and request body, as well as part header and body is separated by a blank line (`\r\n`) 
*   The image data is base64 encoded.

From this obseravation, we can easily construct the upload file request.  

    #!javascript 
    function uploadFacebookPhoto(imageData, caption, accessToken) {

	    var photoUrl = 'https://graph.facebook.com/me/photos?access_token=' + accessToken;
	    var xhr = new XMLHttpRequest();
	    xhr.open("POST", photoUrl, true);
	    xhr.setRequestHeader("Content-Type", "multipart/form-data; boundary=-----")
	    xhr.onreadystatechange = function() {
		    if (xhr.readyState == 4 && xhr.status == 200) {
			    console.log('successfully post the message');
                controller.exit();
		    }
	    };
	    var data = prepareMIMEMessage(imageData, caption, accessToken);
	    xhr.sendAsBinary(data);

    }
    
In the above code, the function `prepareMIMEMessage` does the construction of the message body. 


    

