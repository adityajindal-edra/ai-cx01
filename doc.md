App Automate
Appium API
Apps
Delete an app
Apps
To test your native and hybrid apps on BrowserStack using Appium, you first need to upload an Android app (.apk/.aab file) or an iOS app(.ipa file) to BrowserStack servers. Use our REST API endpoints to upload and manage your apps on BrowserStack.

Upload an app
POST /app-automate/upload

Upload the application under test (AUT) for Appium testing. The supported file formats are .apk and .aab files for Android and .ipa file for iOS. There are two ways to upload an app :

Upload from filesystem : Use this option if the app resides on your local machine or CI/CD server. Learn more about uploading app from filesystem.
Upload using public URL : Use this option when the app is hosted on a remote server (e.g. S3 bucket) and its downloadable via a publicly accessible URL. Learn more about uploading app using public URL.
Request parameters
Request

curl -u "adityajindal_pA0L4w:p7Wx2zrCf4gzbeafn4bZ" \
-X POST "https://api-cloud.browserstack.com/app-automate/upload" \
-F "file=@/path/to/app/file/application-debug.apk" \
-F "custom_id=SampleApp"
-F "ios_keychain_support=true"

Copy
file* File
File to upload. Ensure that the request’s content type is set to multipart/form-data. In cURL, you can do this using -F option. Either file or url parameter is required.

url* String
Remote URL to your app. Ensure that its a publicly accessible URL as BrowserStack will attempt to download the app from this location. Either file or url parameter is required.

custom_id String
Custom ID for the app. Accepted characters are A-Z, a-z, 0-9, ., -, _. All other characters are ignored. Character limit is 100.Refer to our custom ID documentation to know more.

ios_keychain_support String
Setting the parameter to true allows BrowserStack to instrument your app to automatically, clear keychain data after every test session, and handle keychain access groups (changed Bundle Seed ID/Team ID) issues. Refer to our ios-keychain-support documentation to know more.

Response attributes 200 application/json
Response

{
    "app_url": "bs://c8ddcb5649a8280ca800075bfd8f151115bba6b3",
    "custom_id": "SampleApp",
    "shareable_id": "steve/SampleApp"
}

Copy
app_url String
Unique identifier returned upon successful upload of your app on BrowserStack. This value can be used later to specify the application under test in your Appium test scripts.
Example: bs://c8ddcb5649a8280ca800075bfd8f151115bba6b3

custom_id String
Custom ID defined for the uploaded app.
Example: SampleApp. Accepted characters are A-Z, a-z, 0-9, ., -, _. All other characters are ignored. Character limit is 100.

shareable_id String
Shareable ID allows other users in your organization to test an app you uploaded .
Example: steve/SampleApp

List uploaded apps
GET /app-automate/recent_apps

Retrieve a list of recently uploaded apps. BrowserStack retains uploaded apps for 30 days, so you can retrieve all apps uploaded in that timeframe. By default, it returns the last 10 uploaded apps.

Request parameters
Request

curl -u "adityajindal_pA0L4w:p7Wx2zrCf4gzbeafn4bZ" \
-X GET "https://api-cloud.browserstack.com/app-automate/recent_apps"

# List recent apps using customID
curl -u "adityajindal_pA0L4w:p7Wx2zrCf4gzbeafn4bZ" \
-X GET "https://api-cloud.browserstack.com/app-automate/recent_apps/SampleApp"

Copy
custom_id String
Filter uploaded apps by custom ID. Accepted characters are A-Z, a-z, 0-9, ., -, _. All other characters are ignored. Character limit is 100.​

Response attributes 200 application/json
Response

[
    {
        "app_name": "app-debug.apk",
        "app_version": "1.2.0",
        "app_url": "bs://c8ddcb5649a8280ca800075bfd8f151115bba6b3",
        "app_id": "c8ddcb5649a8280ca800075bfd8f151115bba6b3",
        "uploaded_at": "2020-05-05 14:52:54 UTC",
        "custom_id": "SampleApp",
        "shareable_id": "steve/SampleApp"
    },
    {...}
]

Copy
Array
List of recently uploaded apps.

▶ SHOW VALUES
List uploaded apps by group
GET /app-automate/recent_group_apps

Retrieve a list of recently uploaded apps. It returns the last 10 uploaded apps from your BrowserStack group.

Request parameters
Request

curl -u "adityajindal_pA0L4w:p7Wx2zrCf4gzbeafn4bZ" \
-X GET "https://api-cloud.browserstack.com/app-automate/recent_group_apps"

# Limit the number of projects to be displayed using "limit" parameter
curl -u "adityajindal_pA0L4w:p7Wx2zrCf4gzbeafn4bZ" \
-X GET "https://api-cloud.browserstack.com/app-automate/recent_group_apps?limit=5"

Copy
limit String
Specify the number of uploaded apps to fetch. The default value is 10, and the maximum permitted value is 100.

Response attributes 200 application/json
Response

[
    {
        "app_name": "app-debug.apk",
        "app_version": "1.2.0",
        "app_url": "bs://c8ddcb5649a8280ca800075bfd8f151115bba6b3",
        "app_id": "c8ddcb5649a8280ca800075bfd8f151115bba6b3",
        "uploaded_at": "2020-05-05 14:52:54 UTC",
        "custom_id": "SampleApp",
        "shareable_id": "steve/SampleApp"
    },
    {...}
]

Copy
Array
List of recently uploaded apps.

▶ SHOW VALUES
Delete an app
DELETE /app-automate/app/delete/{appID}

Delete an app that was previously uploaded to BrowserStack. Note that apps once deleted cannot be recovered.

Request parameters
Request

curl -u "adityajindal_pA0L4w:p7Wx2zrCf4gzbeafn4bZ" \
-X DELETE "https://api-cloud.browserstack.com/app-automate/app/delete/c8ddcb5649a8280ca800075bfd8f151115bba6b3"

Copy
appID* String
The app ID of the uploaded app

Response attributes 200 application/json
Response

{
    "success": true
}

Copy
success Boolean
Confirmation that app is successfully deleted from BrowserStack servers.