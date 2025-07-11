# =============================================================================================================================
# Set BrowserStack Credentials
# =============================================================================================================================
userName: YOUR_USERNAME
accessKey: YOUR_ACCESS_KEY

# Set 'framework' of your test suite. Example, 'testng', 'cucumber', 'cucumber-testng'
framework: testng # Required only for java based frameworks


# =============================================================================================================================
# Parallels per Platform
# =============================================================================================================================
# The number of parallel threads to be used for each platform set.
# BrowserStack's SDK runner will select the best strategy based on the configured value
#
# Example 1 - If you have configured 3 platforms and set `parallelsPerPlatform` as 2, a total of 6 (2 * 3) parallel threads
# will be used on BrowserStack
#
# Example 2 - If you have configured 1 platform and set `parallelsPerPlatform` as 5, a total of 5 (1 * 5) parallel threads 
# will be used on BrowserStack
parallelsPerPlatform: 1

# =============================================================================================================================
# Android/iOS Application
# =============================================================================================================================
# Specify the app you want to test
# You can pass the app_url, custom_id or shareable_id obtained on uploading the app on BrowserStack
app: bs://5f5w7g3s5a9b5g6f39fk0 #passing app_url
app: CalculatorApp #Passing custom_id
app: exampleuser/CalculatorApp #Passing shareable_id
app: /path/to/app/file/application-debug.apk #Passing absolute path from your local filesystem
app: ./LocalSample.apk #Passing relative path

# Specify the app path with the custom_id
app:
  path: /Path/to/app
  custom_id: custom_id 

# If you’re using custom_id or shareable_id for your app value, and you have different versions of the app, 
# please use appVersion to configure which version your test needs to run on.
appVersion: 2.0

# =============================================================================================================================
# Platforms (devices to test)
# =============================================================================================================================
# Platforms object contains all the device combinations you want to test on.

# For Android Devices
platforms:
  - platformName: android
    deviceName: Samsung Galaxy S22 Ultra
    platformVersion: 12.0
  - platformName: android
    deviceName: Google Pixel 7 Pro
    platformVersion: 13.0

# For iOS Devices
platforms:
  - platformName: ios
    deviceName: iPhone 14 Pro Max
    platformVersion: 16
  - platformName: ios
    deviceName: iPhone XS
    platformVersion: 15


# =============================================================================================================================
# BrowserStack Reporting 
# =============================================================================================================================

#Set 'projectName' to the name of your project.
projectName: BrowserStack Samples 

#Set 'buildName' to the name of your project.
buildName: browserstack build 

# buildIdentifier` is a unique id to differentiate every execution that gets appended to buildName. 
# Choose your buildIdentifier format from the available expressions:
# ${BUILD_NUMBER} (Default): Generates an incremental counter with every execution
# ${DATE_TIME}: Generates a Timestamp with every execution. Eg. 05-Nov-19:30
buildIdentifier: '${BUILD_NUMBER}'


# =============================================================================================================================
# Test Configuration Capabilities
# =============================================================================================================================

# Set browserStackLocal to true if mobile apps need to access resources hosted in development or testing environments 
# during automated test execution.
browserstackLocal: true # <boolean> (Default true)
# Options to be passed to BrowserStack local in-case of advanced configurations
browserStackLocalOptions:
  forcelocal: true  # <boolean> (Default: false) Set to true to resolve all your traffic via BrowserStack Local tunnel.
  localIdentifier: randomstring # <string> Needed if you need to run multiple instances of local.
  proxyHost: 127.0.0.1 
  proxyPort: 8000
  proxyUser: user
  proxyPass: password
  -pac-file: <pac_file_abs_path> #<string> Pass the absolute path of PAC file for proxy server related decisioning
  f: /my/awesome/folder # <string> Pass the path of test HTML files on BrowserStack local.

appiumVersion: 2.0.0 #(select between multiple options) # Set the Appium version in your test scripts. 
# For supported Appium versions, visit https://www.browserstack.com/app-automate/capabilities
idleTimeout: 90 # default timeout is 90 secs, it can be edited to higher(upto 300s) or a lower value for your tests
acceptInsecureCerts: true # <boolean> # Avoid invalid certificate errors while using self-signed certificate to test your app.
httpProxy: http://user:pwd@127.0.0.1:1234  #Add the proxy parameters in the adjacent format to use httpProxy
httpsProxy: https://user:pwd@127.0.0.1:1234  #Add the proxt parameters in the adjacent format to use httpsProxy

# =============================================================================================================================
# Debugging options
# =============================================================================================================================

video: true # <boolean> # Set to true enable video recording during your test
debug: true # <boolean> # Set to true to enable automatic screenshots for various appium commands
networkLogs: true # <boolean> # Set to true to capture network logs for your test
deviceLogs: true  # <boolean> # Set to true to enable capture of device logs for your test
appiumLogs: true  # <boolean> # Set to true to enable capture of raw appium logs for your test
captureContent: false # <boolean> # Set to true to capture response payload in network logs


# =============================================================================================================================
# Device Feature Capabilities
# =============================================================================================================================

# If you upload an iOS app to BrowserStack servers using REST API, Browserstack will re-sign the app with 
# a self provisioning profile to install your app on our devices during test execution. 
# This process will result in removal of entitlements from your iOS app. Set this capability to false to disable 
# resigning of your Enterprise signed 'app' so that you can test features like, push notifications on BrowserStack devices.
resignApp: true # <boolean> # Only for iOS 
customNetwork: 1000
networkProfile: 4g-lte-advanced-good #(select between multiple options) # Required if you want to simulate different network conditions
deviceOrientation: portrait # select between portrait/landscape # Set the screen orientation of mobile device
geoLocation: US #(select between multiple options) # Set to test how your app behaves in specific countries
timezone: New_York #(select between multiple options) # Configure tests to run on a custom time zone
language: Fr  #(select between multiple options) #Set the language of the app under test
locale: Fr #(select between multiple options) #Set device locale

# =============================================================================================================================
# Appium Capabilities
# =============================================================================================================================

automationName: UIAutomator2 # Set the automation engine to use
# Supported values: UIAutomator2(Android Default), XCUITest(iOS Default), Appium, Flutter, YouiEngine, UIAutomator1

autoGrantPermissions: true # Set to true for Appium to automatically determine which permissions your app requires 
#and grant them to the app on install.

newCommandTimeout: 60 #Set the value in seconds to wait for a new command before ending the session

# Note: All Appium supported capabilities can be used with BrowserStack SDK

# =============================================================================================================================
# Test Reporting & Analytics
# =============================================================================================================================
  
# Test Reporting & Analytics is an intelligent test reporting & debugging product. It collects data using the SDK.
# Visit automation.browserstack.com to see your test reports and insights. To disable Test Reporting & Analytics, 
# specify `testObservability: false` in the key below.
# Read about what data is collected at https://www.browserstack.com/docs/test-reporting-and-analytics/references/terms-and-conditions
# Check the available frameworks here: https://www.browserstack.com/docs/test-reporting-and-analytics/overview/what-is-test-reporting-and-analytics

testObservability: true 
Capabilities Reference

Appium - BrowserStack SDK

BrowserStack specific capabilities	 
SDK-Capability	Values
userName
For running your Selenium and Appium tests on BrowserStack it, requires a username and an access key for authenticating the user. This capability can be used to set the username.	You can find your username and access key on the Settings page under the Automate section.

Example: userName: <BROWSERSTACK_USERNAME>
accessKey
For running your Selenium and Appium tests on BrowserStack it, requires a username and an access key for authenticating the user. This capability can be used to set the access key.	You can find your username and access key on the Settings page under the Automate section.

Example: accessKey: <BROWSERSTACK_ACCESSKEY>
framework
Specify the language framework for your test.	This capability is applicable only for Java language.

Example:
framework: testng
app
Specify the app you want to test.	You can pass the app_url, custom_id or shareable_id obtained on uploading the app on BrowserStack.

Example:
app:
   path: /Path/to/app
   custom_id: custom_id
appVersion
Configure which version your test needs to run on.	Use appVersion if you’re using custom_id or shareable_id for your app value, and you have different versions of the app.

Example:
appVersion: 2.0
parallelsPerPlatform
Specify the number of parallel threads to be used for each platform set.	Use appVersion if you’re using custom_id or shareable_id for your app value, and you have different versions of the app.

Example:
parallelsPerPlatform: 1
Test configuration capabilities	 
SDK-Capability	Values
projectName
Allows the user to specify a name for a logical group of builds.	Default: Untitled Project

Example: projectName: BrowserStack Sample
buildName
Allows the user to specify a name for a logical group of tests.	Default: Untitled Build

Example: buildName: browserstack-build-1
buildIdentifier
A unique identifier to logically group multiple test sessions together.	Default: Untitled Build

Example: buildIdentifier: browserstack-build--identifier-1
buildTag
A custom tag for your builds.	Default: Untagged Build

Example: buildTag: browserstack-build-tag
browserstackLocal
Use this capability to test your locally hosted websites on BrowserStack by setting the value to true. To enable access to the local machine you need to setup BrowserStack Local binary.	true, false
Default: false

Example: browserstackLocal: true
forcelocal
Use this capability to resolve all your traffic via BrowserStack Local tunnel.	String
Default: false

Example:
browserStackLocalOptions:
   forcelocal: true
localIdentifier
Use this capability to specify the unique Local Testing connection name in your test.	String
Default: false

Example:
browserStackLocalOptions:
   localIdentifier: local_connection_name
debug
Required if you want to generate screenshots at various steps in your test.	true, false
Default: false

Example: debug: false
networkLogs
Required if you want to capture network logs for your test. Network Logs are supported for all desktop browsers, Android and iOS devices with a few exceptions - IE 10 on any OS; IE 11 on Windows 7 / 8.1 and any browser on MacOS High Sierra and Mojave.	true, false
Default: false

Example: networkLogs: false

Note: You may experience minor reductions in performance when testing with Network Logs turned on with Desktop sessions.
video
Required if you want to enable video recording during your test.	true, false
Default: true

Example: video: true
deviceLogs
Capture device logs for your test.	true, false
Default: true
appiumLogs
Capture raw Appium logs for your test.	true, false
Default: true
captureContent
Capture response payload in network logs.	true, false
Default: true
geoLocation
Use this capability to simulate website and mobile behavior from different locations. Traffic to your website or mobile app will originate from an IP address hosted in the country you have chosen.	“CN” for China, “FR” for France, “IN” for India and “US” for United States of America and so on. View the list of 65+ supported countries.

Example: geoLocation: CN

Note: This capability is available with enterprise plans only.
timezone
Use this capability to run your tests on a custom timezone.	New_York for America/New_York, London for Europe/London, Kolkata for Asia/Kolkata. Set the city name as value.

You can view the complete list of timezones on Wikipedia. Example: timezone: New_York

Note: This feature is not supported on the following devices: [“Oppo Reno 6”, “Xiaomi Redmi Note 9”, “Xiaomi Redmi Note 11”, “Huawei P30”, “Huawei P30”, “Huawei P30”, “Oppo Reno 3 Pro”, “Realme 8”, “Xiaomi Redmi Note 10S”, “Xiaomi Redmi Note 7 Pro”, “Xiaomi Redmi Note 12 Pro Plus”, “Xiaomi Redmi Note 12 Pro”, “Xiaomi Redmi Note 12 4G”, “Xiaomi Redmi Note 10 Pro”, “Xiaomi Redmi Note 9 Pro Max”, “Xiaomi Redmi Note 5 Pro”]
idleTimeout
BrowserStack triggers BROWSERSTACK_IDLE_TIMEOUT error when a session is left idle for more than 90 seconds. This happens as BrowserStack by default waits for the timeout duration for additional steps or commands to run, if we do not receive any command during that time, the session is stopped, changing the session status to TIMEOUT on the Automate dashboard.

This capability can be used to modify the timeout value.	0 to 300 seconds
Default: 90 seconds

Example: idleTimeout: 30
acceptInsecureCerts
Avoid invalid certificate errors while using self-signed certificate to test your app.	Example: acceptInsecureCerts: true
Mobile capabilities	 
SDK-Capability	Values
deviceName
Specifies a particular mobile device for the test environment.	Example:

platforms:
   - deviceName: iPhone 13
View the list of supported devices.
platforms
Specify all the device combinations you want to test on.	Example:

platforms:
   - deviceName: iPhone 13
View the list of supported devices.
platformName
Specify all the device combinations you want to test on..	Example:

platforms:
   - platformName: android
View the list of supported devices.
platformVersion
Specifies a particular mobile device for the test environment.	Example:

platforms:
   - platformVersion: 14.0
View the list of supported devices.
deviceOrientation
Set the screen orientation of mobile device.	portrait, landscape
Default: portrait

Example: deviceOrientation: portrait
customNetwork
Required if you want to simulate the custom network condition.	Example: customNetwork: 1000

Note: The supported operating systems are iOS and Android.
networkProfile
Required if you want to simulate different network conditions.	Example: networkProfile: 2g-gprs-good
View the list of supported network profiles.

Note: The supported operating systems are iOS and Android. no-network capability is available on all android devices and in ios v11 and above devices. The airplane-mode capability is only available on android devices.
Miscellaneous capabilities	 
SDK-Capability	Values
appProfiling
Enable detailed app performance profiling.	Example:

appProfiling: true
interactiveDebugging
Interact, and debug any ongoing test session.	Example:

interactiveDebugging: true
gpsLocation
Simulate the location of the device to a specific GPS location.	Example:

gpsLocation: -73.935242,40.730610
appStoreConfiguration
Example:

appStoreConfiguration
   username: "your_email"
   password: "your_password"
midSessionInstallApps
Install app(s) in between a test session. Upload your apps to BrowserStack servers using REST API. Use the app_url value returned as a result of the upload request to set this capability.	Example:

midSessionInstallApps:
   - bs://<hashed app-id>
enableBiometric
Enable Biometric Authentication.	Example:

enableBiometric: true
enablePasscode
Use passcode-protected devices to run tests.	Example:

enablePasscode: true
updateIosDeviceSettings
Set darkMode configuration to "true" inside the updateIosDeviceSettings capability to enable dark mode setting on the device	Example:

updateIosDeviceSettings
   darkMode: true
enableApplePay
Test Apple Pay in your test session.	Example:

enableApplePay: true
nativeWebTap
Enable this capability if you are unable to get Apple Pay payment screen after clicking the Apple Pay button.	Example:

nativeWebTap: true
enableAudioInjection
Use your audio files in the test.	Example:

enableAudioInjection: true
enableSim
Obtain a device with SIM	Example:

enableSim: true
simOptions
Set the configuration “region” to the mentioned country name to obtain a SIM device for that country.	Example:

simOptions
   region: USA
   esim: true
testObservability
Advanced test reporting and debugging tool that helps you analyze test failures dramatically faster.	Example:

testObservability: true