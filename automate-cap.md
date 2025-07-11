Capabilities reference gist file

Expand this section to check out the list of supported Capabilities
# =============================================================================================================================
# Set BrowserStack Credentials
# =============================================================================================================================
userName: YOUR_USERNAME
accessKey: YOUR_ACCESS_KEY

# Set `framework` of your test suite. Example, `testng`, `cucumber`, `cucumber-testng`
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
# Platforms (Browsers / Devices to test)
# =============================================================================================================================
# Platforms object contains all the browser / device combinations you want to test on.

platforms:
  - os: OS X
    osVersion: Big Sur
    browserName: Chrome
    browserVersion: latest
    # ===============================================
    # Chrome Browser Specific Capabilities (OPTIONAL)
    # ===============================================
    chrome:
      driver: 112.0.5615.28
    chromeOptions: 
      args:                      
        - --start-maximized
    # ===============================================  
  - os: Windows
    osVersion: 11
    browserName: Edge
    browserVersion: latest
    # ===============================================
    # Edge Browser Specific Capabilities (OPTIONAL)
    # ===============================================
    edge: 
      enablePopups: false #<boolean> (Default: X) Set to true if you want to enable Popups
      enableSidebar: false #<boolean> (Default: X) Set to true if you want to enable sidebar
    # ===============================================        
  - os: Windows
    osVersion: 10
    browserName: Firefox
    browserVersion: latest
    # ===============================================
    # Firefox Browser Specific Capabilities (OPTIONAL)
    # ===============================================
    firefox: 
      driver: 0.32.0 #Set the driver version you want to use
    # ===============================================        
  - os: OS X
    osVersion: Big Sur
    browserName: Safari
    browserVersion: 14.1
    # ===============================================
    # Safari Browser Specific Capabilities (OPTIONAL)
    # ===============================================
    safari:
      driver: 2.45 #Set the driver version you want to use
      enablePopups: false #<boolean> (Default: X) Set to true if you want to enable Popups
      allowAllCookies: false #<boolean> (Default: false) Set to true if you want to allow all cookies
    # ===============================================        

# =============================================================================================================================
# BrowserStack Reporting 
# =============================================================================================================================
#Set 'projectName' to the name of your project.
projectName: BrowserStack Samples 

#Set 'projectName' to the name of your project.
buildName: browserstack build 

# buildIdentifier` is a unique id to differentiate every execution that gets appended to buildName. 
# Choose your buildIdentifier format from the available expressions:
# ${BUILD_NUMBER} (Default): Generates an incremental counter with every execution
# ${DATE_TIME}: Generates a Timestamp with every execution. Eg. 05-Nov-19:30
buildIdentifier: '${BUILD_NUMBER}'

# =============================================================================================================================
# BrowserStack Local (For localhost, staging/private websites)
# =============================================================================================================================

# Set browserStackLocal to true if your website under test is not accessible publicly over the internet
browserstackLocal: true # <boolean> (Default true)
# Options to be passed to BrowserStack local in-case of advanced configurations
browserStackLocalOptions:
  forcelocal: true  # <boolean> (Default: false) Set to true to resolve all your traffic via BrowserStack Local tunnel.
  localIdentifier: randomstring # <string> (Default: null) Needed if you need to run multiple instances of local.
  proxyHost: 127.0.0.1 
  proxyPort: 8000
  proxyUser: user
  proxyPass: password
  -pac-file: <pac_file_abs_path> #<string> Pass the absolute path of PAC file for proxy server related decisioning
  f: /my/awesome/folder # <string> Pass the path of test HTML files on BrowserStack local.
  verbose: 3
  -use-ca-certificate: <path_to_pem_file>
  -use-system-installed-ca: true
  -log-file: <path_to_log_file>

# =============================================================================================================================
# Debugging features
# =============================================================================================================================
debug: false # <boolean> # Set to true if you need screenshots for every selenium command ran
networkLogs: false # <boolean> Set to true to enable HAR logs capturing
consoleLogs: errors # <string> Remote browser's console debug levels to be printed (Default: errors)
# Available options are `disable`, `errors`, `warnings`, `info`, `verbose` (Default: errors)  

# =============================================================================================================================
# TEST CONFIGURATION CAPABILITIES
# =============================================================================================================================
video: true
seleniumLogs: true
telemetryLogs: true
geoLocation: CN
timezone: New_York 
resolution: 1024x768
idleTimeout: 30
maskCommands: setValues, getValues, setCookies, getCookies
maskBasicAuth: true
autoWait: 35
hosts: 1.2.3.4 staging.website.com
bfcache: 1
wsLocalSupport: true
disableCorsRestrictions: true
httpProxy: http://user:pwd@127.0.0.1:1234  #Add the proxy parameters in the adjacent format to use httpProxy
httpsProxy: https://user:pwd@127.0.0.1:1234  #Add the proxt parameters in the adjacent format to use httpsProxy
# =============================================================================================================================
# MOBILE SPECIFIC CAPABILITIES
# =============================================================================================================================

# Set the screen orientation of mobile device.
deviceOrientation: portrait # select between portrait/landscape
# Required if you want to simulate the custom network condition.
customNetwork: 1000 #download speed (kbps), upload speed (kbps), latency (ms), packet loss (%)
# Required if you want to simulate different network conditions.
networkProfile: 2g-gprs-good #(select between multiple options)

# =============================================================================================================================
# BROWSER SPECIFIC CAPABILITIES
# =============================================================================================================================

# Browser specific capabilities have to be strictly placed with respective platform capabilites inside the platforms object 

# ===============================================
# Chrome Browser Specific Capabilities
# ===============================================
# platforms:
#   - os: OS X
#     osVersion: Big Sur
#     browserName: Chrome
#     browserVersion: latest
#     #Chrome specific capabilities
#     chrome: 
#       driver: 112.0.5615.28
#     chromeOptions: 
#       args:                      
#         - incognito
#         - --start-maximized
#       perfLoggingPrefs:
#       enableNetwork: false

# ===============================================
# Edge Browser Specific Capabilities 
# ===============================================
# platforms:
#   - os: Windows
#     osVersion: 11
#     browserName: Edge
#     browserVersion: 111.0
#     # Edge specific capabilities
#     edge: 
#       enablePopups: false #<boolean> (Default: X) Set to true if you want to enable Popups
#       enableSidebar: false #<boolean> (Default: X) Set to true if you want to enable sidebar

# ===============================================
# Safari Browser Specific Capabilities 
# ===============================================
# platforms:
#   - os: OS X
#     osVersion: Big Sur
#     browserName: Safari
#     browserVersion: 14.1
#     # Safari Specific Capabilities (OPTIONAL)
#     safari:
#       driver: 2.45 #Set the driver version you want to use
#       enablePopups: false #<boolean> (Default: X) Set to true if you want to enable Popups
#       allowAllCookies: false #<boolean> (Default: false) Set to true if you want to allow all cookies

# ===============================================
# Firefox Browser Specific Capabilities 
# ===============================================

# platforms:
#   - os: Windows
#     osVersion: 10
#     browserName: Firefox
#     browserVersion: latest
#   # Firefox specific capabilities (Optional)
#     firefox: 
#       driver: 0.32.0 #Set the driver version you want to use

# ===============================================
# IE Browser Specific Capabilities 
# ===============================================      
# platforms:
#   - os: Windows
#     osVersion: 10
#     browserName: IE
#     browserVersion: 11.0
#     # IE specific capabilities (OPTIONAL)
#     ie: 
#       driver: 4.0.0 
#       noFlash: false #<boolean> (Default: X) Set to true if you want to enable flash
#       compatibility: <value>
#       arch: <value>
#       enablePopups: false #<boolean> (Default: X) Set to true if you want to enable Popups
#       enableSidebar: false #<boolean> (Default: X) Set to true if you want to enable sidebar
#       sendKeys: true #<boolean> (Default: X) Allows to type content automatically into editable field while executing tests.


# =============================================================================================================================
# Test Reporting & Analytics
# =============================================================================================================================

# Test Reporting & Analytics is an intelligent test reporting & debugging product. It collects data using the SDK.
# Visit automation.browserstack.com to see your test reports and insights. To disable Test Reporting & Analytics, 
# specify `testObservability: false` in the key below.
# Read about what data is collected at https://www.browserstack.com/docs/test-reporting-and-analytics/references/terms-and-conditions
testObservability: true 
Capabilities Reference

Selenium - BrowserStack SDK

BrowserStack specific capabilities	 
SDK-Capability	Values
userName
For running your Selenium and Appium tests on BrowserStack it, requires a username and an access key for authenticating the user. This capability can be used to set the username.	You can find your username and access key on the Settings page under the Automate section.

Example: userName: <BROWSERSTACK_USERNAME>
accessKey
For running your Selenium and Appium tests on BrowserStack it, requires a username and an access key for authenticating the user. This capability can be used to set the access key.	You can find your username and access key on the Settings page under the Automate section.

Example: accessKey: <BROWSERSTACK_ACCESSKEY>
os
OS you want to test.	Windows, OS X
osVersion
OS version you want to test.	Windows: XP, 7, 8, 8.1, 10 and 11
OS X: Snow Leopard, Lion, Mountain Lion, Mavericks, Yosemite, El Capitan, Sierra, High Sierra, Mojave, Catalina, Big Sur, Monterey, Ventura, Sonoma, Sequoia and Tahoe

Example:

platforms:
  - os: Windows
       osVersion: 10
Test configuration capabilities	 
SDK-Capability	Values
projectName
Allows the user to specify a name for a logical group of builds.	Default: Untitled Project

Example: projectName: BrowserStack Sample
buildName
Allows the user to specify a name for a logical group of tests.	Default: Untitled Build

Example: buildName: browserstack-build-1
browserstackLocal
Use this capability to test your locally hosted websites on BrowserStack by setting the value to true. To enable access to the local machine you need to setup BrowserStack Local binary.	true, false
Default: false

Example: browserstackLocal: true
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
consoleLogs
Required if you want to capture browser console logs at various steps in your test. Console Logs are available for Selenium tests on Desktop Chrome and Mobile Chrome (Android devices).	disable, errors, warnings, info, verbose
Default: errors

Example: consoleLogs: errors

disable: stops capturing the console logs
errors: shows only error output in console
warnings: shows warning and error output in the console
info: shows info statement, warning and error output in the console
verbose: shows all console output
networkLogs
Required if you want to capture network logs for your test. Network Logs are supported for all desktop browsers, Android and iOS devices with a few exceptions - IE 10 on any OS; IE 11 on Windows 7 / 8.1 and any browser on MacOS High Sierra and Mojave.	true, false
Default: false

Example: networkLogs: false

Note: You may experience minor reductions in performance when testing with Network Logs turned on with Desktop sessions.
video
Required if you want to enable video recording during your test.	true, false
Default: true

Example: video: true
seleniumLogs
Required if you want to enable selenium logs for your desktop browser tests.	true, false
Default: true
telemetryLogs
Required if you want to capture telemetry logs for your test. Telemetry Logs are supported for all desktop browsers on any OS except for Windows XP and all MacOS versions below Sierra.	true, false
Default: false

Example: telemetryLogs: true

Note: Only Selenium versions 4.0.0-alpha-6 and above are supported.
geoLocation
Use this capability to simulate website and mobile behavior from different locations. Traffic to your website or mobile app will originate from an IP address hosted in the country you have chosen.	“CN” for China, “FR” for France, “IN” for India and “US” for United States of America and so on. View the list of 65+ supported countries.

Example: geoLocation: CN

Note: This capability is available with enterprise plans only.
timezone
Use this capability to run your tests on a custom timezone.	New_York for America/New_York, London for Europe/London, Kolkata for Asia/Kolkata. Set the city name as value.

You can view the complete list of timezones on Wikipedia. Example: timezone: New_York

Note: This feature is not supported on the following devices: [“Oppo Reno 6”, “Xiaomi Redmi Note 9”, “Xiaomi Redmi Note 11”, “Huawei P30”, “Huawei P30”, “Huawei P30”, “Oppo Reno 3 Pro”, “Realme 8”, “Xiaomi Redmi Note 10S”, “Xiaomi Redmi Note 7 Pro”, “Xiaomi Redmi Note 12 Pro Plus”, “Xiaomi Redmi Note 12 Pro”, “Xiaomi Redmi Note 12 4G”, “Xiaomi Redmi Note 10 Pro”, “Xiaomi Redmi Note 9 Pro Max”, “Xiaomi Redmi Note 5 Pro”]
resolution
Set the resolution of VM before beginning of your test.	Windows (XP): 800x600, 1024x768, 1280x800, 1280x1024, 1366x768, 1440x900, 1680x1050, 1600x1200, 1920x1200, 1920x1080, 2048x1536, 2560x1600, 2800x2100

Windows (7):800x600, 1024x768, 1280x800, 1280x1024, 1366x768, 1440x900, 1680x1050, 1600x1200, 1920x1200, 1920x1080, 2048x1536, 2560x1600, 2800x2100, 3840x2160

Windows (8,8.1,10,11): 1024x768, 1280x800, 1280x1024, 1366x768, 1440x900, 1680x1050, 1600x1200, 1920x1200, 1920x1080, 2048x1536, 2560x1600, 2800x2100, 3840x2160

OS X (Tahoe,Sequoia,Sonoma,Ventura,Monterey,Big Sur,Catalina,Mojave,High Sierra): 1024x768, 1280x960, 1280x1024, 1600x1200, 1920x1080, 2560x1440, 2560x1600, 3840x2160

OS X (All other versions): 1024x768, 1280x960, 1280x1024, 1600x1200, 1920x1080

Default:1920x1080

Example: resolution: 1024x768
maskCommands Use this capability to mask the data sent or retrieved by certain commands.	Default:Empty Array

setValues
All the text send via sendKeys command will be redacted.

getValues
All the text retrieved via get command will be redacted.

setCookies
All the cookies which are set by the addCookie command will be redacted.

getCookies
All the cookie values obtained using the getCookies and getCookieNamed command will be redacted.

Example:
maskCommands: setValues, getValues, setCookies, getCookies

Note: You can pass multiple commands in a single array, separated by commas. Sensitive data in certain logs (like Selenium, Appium, video, etc.) cannot be masked. View our documentation to disable these logs instead.
idleTimeout
BrowserStack triggers BROWSERSTACK_IDLE_TIMEOUT error when a session is left idle for more than 90 seconds. This happens as BrowserStack by default waits for the timeout duration for additional steps or commands to run, if we do not receive any command during that time, the session is stopped, changing the session status to TIMEOUT on the Automate dashboard.

This capability can be used to modify the timeout value.	0 to 300 seconds
Default: 90 seconds

Example: idleTimeout: 30
maskBasicAuth
If you use basic authentication in your test cases, the username and password would be visible in text logs. Use this capability to mask those credentials.	true, false
Default: false

To mask the credentials set the capability to “true”.
Example: maskBasicAuth: true
autoWait
Use this capability to specify a custom delay between the execution of Selenium commands.	Default: 20 seconds

Example: autoWait: 35
hosts
Use this capability to add host entry (/etc/hosts) in remote BrowserStack machine.

For example, if you use staging.website.com in test cases but do not have a DNS entry for the domain and the public IP, you can use this capability to add host entry in the machine.	<IP_address Domain_name>

Example: hosts: 1.2.3.4 staging.website.com

Note: Supported only on desktop machines.
bfcache
IE 11 browser uses cached pages when you navigate using the backward or forward browser buttons. You can use this capability to disable the use of cached pages.	0 and 1
Default: 0

To disable page caching set value as 1
Example: bfcache: 1
wsLocalSupport
Chrome browser v71 and above have changed the way PAC files are supported. Use this capability to enable WSS (WebSocket Secure) connections to work with Network Logs on Chrome browser v71 and above.

If you are using localhost in your test, change it to bs-local.com	true, false
Default: false

Example: wsLocalSupport: true

Note: This capability is only valid for Chrome browsers v71 and above.
disableCorsRestrictions
Use this capability to disable cross origin restrictions in Safari. Available for Tahoe, Sequoia, Sonoma, Ventura, Monterey, Big Sur, Catalina and Mojave.	true, false
Default: false

Example: disableCorsRestrictions: true
Mobile capabilities	 
SDK-Capability	Values
deviceName
Specifies a particular mobile device for the test environment.	Example:

platforms:
   - deviceName: iPhone 13
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
Browser capabilities	 
SDK-Capability	Values
browserName
Run your tests on a specific browser by setting the browser name as the value.	Firefox, Safari, IE, Chrome, Opera, Edge, Chromium
browserVersion
Run your tests on a specific browser version by setting the browser version as the value.

Note: browserVersion capability is applicable for desktop browsers only.	latest-beta, latest, latest-1, latest-2 or so on.
Use latest-beta or latest [-n number] format to automatically choose the current beta release of the browser or the latest (and other older) browser versions available on BrowserStack without having to change code. A common use case is to run tests on the latest browser versions and the beta versions for frequently updated browsers such as Chrome and Firefox.

Example:

platforms:
  - os: Windows
       osVersion: 11
       browserName: Chrome
       browserVersion: 103.0

Specific browser version
Pass a particular browser version number.
Example:

browserVersion: 11.0 #for IE-11 browser

Default: Latest stable version of browser is used.

Note: latest-beta, latest, latest-1, and other latest flags are dependent on the selected OS and OS Version. For example, on Windows 10, IE browser, the latest version would be 11.0, and on OS X Mojave, Safari browser, the latest version would be 12.0

View the list of latest browser versions.
Parameter override rules
- osVersion can only be defined when os has been defined.

- Default browser is Chrome when no browser is passed by the user or the Selenium API (implicitly).

- If consoleLogs is enabled it will take precedence over Logging Preferences of type BROWSER that you may have set in your test script.