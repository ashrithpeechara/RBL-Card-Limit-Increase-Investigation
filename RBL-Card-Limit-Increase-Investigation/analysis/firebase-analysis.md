# Firebase Realtime Database Security Analysis Report

**Investigation:** RBL-Themed Android APK Investigation  
**Component:** Firebase Realtime Database  
**Assessment Type:** Static Analysis and Read-Only Endpoint Inspection  
**Assessment Date:** 03 November 2026  
**Status:** Sensitive Data Exposure Observed — Attribution Verification Pending  
**Classification:** Confidential — Contains Sensitive Evidence

---

## 1. Executive Summary

During the investigation of the Android application labelled **RBL CARD LIMIT INCREASE**, a Firebase Realtime Database endpoint associated with the project identifier `rbl-card-73-29-7-26` was examined.

A request to the database root JSON endpoint returned a JSON response containing actual database records rather than an empty response or a permission-denied message.

The returned data included:

- Administrative credential information.
- Android device identifiers and device metadata.
- SIM card numbers and carrier information.
- SMS records, including message content.
- SMS forwarding configuration.
- Call-forwarding-related configuration indicators.

The observed response indicates a potentially serious database access-control failure. If the endpoint returned these records without authentication, an external party capable of reaching the endpoint could potentially access sensitive user information.

The database response alone does not establish who owns or operates the Firebase project, whether the APK created it, or whether all returned records originated from the investigated application.

**Preliminary conclusion:** Sensitive information was returned by the tested Firebase database root endpoint. Unauthenticated exposure is the leading security concern, subject to confirmation of the request's authentication context.

---

## 2. Investigation Scope

The investigation focused on:

1. Identifying Firebase-related indicators in the recovered APK.
2. Identifying application components associated with SMS and call forwarding.
3. Examining the Firebase Realtime Database endpoint.
4. Recording the structure and categories of data returned.
5. Assessing potential confidentiality and privacy impacts.
6. Preserving the response and its cryptographic hashes.

The investigation was limited to read-only inspection. No database records were modified, and no SMS messages or forwarding commands were submitted.

---

## 3. Firebase Project Identification

**Firebase project identifier:**

`rbl-card-73-29-7-26`

**Database hostname:**

`rbl-card-73-29-7-26-default-rtdb.firebaseio.com`

**Root JSON endpoint:**

`https://rbl-card-73-29-7-26-default-rtdb.firebaseio.com/.json`

The hostname follows the Firebase Realtime Database default hostname pattern.

The project identifier and endpoint were supplied during the investigation. Their association with the APK must be established through application configuration, runtime network evidence, or another independent artifact.

---

## 4. Endpoint Response Analysis

A GET request was made to the Firebase database root JSON endpoint.

The response was saved locally for evidence preservation.

### 4.1 Response metadata

The previously captured response headers included:

| Header | Observed value |
|---|---|
| Cache-Control | no-cache |
| Content-Type | application/json; charset=utf-8 |
| Content-Length | 2242674 |
| Server | nginx |
| Strict-Transport-Security | max-age=31536000; includeSubDomains; preload |
| Access-Control-Allow-Origin | * |

The reported content length was approximately 2.24 MB.

### 4.2 Interpretation

- `Content-Type: application/json` indicates that the response was delivered as JSON.
- `Content-Length: 2242674` indicates a substantial response body.
- `Access-Control-Allow-Origin: *` permits cross-origin browser requests under the applicable CORS rules. It does not independently prove unauthenticated database access.
- The server and transport headers provide response metadata but do not establish the identity of the database operator.

The decisive evidence is the returned JSON content, not the headers alone.

**Important verification limitation:** The HTTP status code and complete authentication context must be retained alongside the response. The supplied output excerpt does not independently display the HTTP status code.

---

## 5. Database Structure and Sensitive Information

The beginning of the returned JSON showed the following top-level objects:

- `number`
- `password`
- `users`

These objects expose several categories of sensitive information.

### 5.1 Administrative credential information

The response included:

`password.admin_pass`

The returned sample contained a populated value.

**Security significance:**

Exposure of an administrative credential may allow unauthorized access to an associated application administration interface or other functionality if the credential is valid and reused.

However, the investigation has not established whether this value is valid, what system it authenticates to, or whether it provides administrative access to Firebase itself.

The credential must not be tested or reused.

### 5.2 Device information

Records under the `users` hierarchy contained device metadata, including:

| Field | Description |
|---|---|
| `device_id` | Device identifier |
| `android_version` | Android operating system version |
| `app_version` | Application version |
| `brand` | Device brand |
| `manufacturer` | Device manufacturer |
| `model` | Device model |
| `battery` | Battery percentage |
| `network_type` | Network connection type |
| `last_seen` | Last-seen timestamp |
| `created_at` | Record creation timestamp |

This information can expose device profiles and usage-related metadata.

### 5.3 SIM card information

The observed records contained:

- SIM 1 carrier.
- SIM 1 phone number.
- SIM 2 carrier.
- SIM 2 phone number.

At least one returned device record contained an Indian mobile number.

**Security significance:**

Phone numbers and carrier details are personally identifiable information. Their exposure can increase the risk of targeted social engineering, SIM-related fraud and user profiling.

### 5.4 SMS records

The returned JSON included an `all_sms` hierarchy.

The visible sample contained:

- Device identifiers.
- Message timestamps.
- Message content.
- Direction-related record identifiers.
- Nested message collections.

The visible message excerpt appeared to contain OTP-related content.

**Security significance:**

SMS records may contain authentication codes, financial notifications, personal communications and account-related information.

Exposure of these records represents a serious confidentiality risk.

The investigation did not attempt to validate or use any exposed OTP.

### 5.5 SMS forwarding configuration

The response contained a field:

` sms_forward `

One observed value was:

`both`

This is evidence that the database stores an SMS forwarding configuration indicator.

The exact meaning of every possible value must be confirmed from the application implementation. The value alone does not prove that forwarding was active on the corresponding device at the time of inspection.

### 5.6 Call-forwarding configuration

The earlier APK code analysis identified a Firebase-related call-forwarding data path:

`users/{device_id}/call_forward/{value}`

The application-side implementation referenced fields including:

- `forward_number`
- `sim_slot`
- `action`
- `status`

This establishes that the recovered application contains call-forwarding-related functionality.

It does not independently establish that a particular database record successfully activated call forwarding on a device.

---

## 6. Correlation with APK Analysis

The APK investigation identified several application components associated with Firebase-backed functionality.

| Application component | Observed functionality |
|---|---|
| `CallForwardManager` | Call-forwarding management |
| `SmsListenerService` | SMS-related service functionality |
| `SmsNForward` | SMS forwarding-related functionality |
| `SmsSendManager` | SMS sending functionality |
| `MyApp` | Application initialization |
| `FirebaseInitProvider` | Firebase initialization provider |

The earlier static analysis also identified database-related paths and application strings, including:

- `all_sms`
- `call_forward`
- `forward_number`
- `CHECK_FORWARD_NUMBER`
- `UPDATE_FORWARD_NUMBER`
- `CLEAR_FORWARD_NUMBER`
- `STOP_FORWARDING`

These indicators support the presence of SMS and call-forwarding functionality in the recovered application.

**Attribution limitation:** The Firebase SDK references and application functionality do not, by themselves, prove that the investigated APK communicates with the specific project identified above. A direct project-to-APK association requires additional configuration or network evidence.

---

## 7. Security Findings

### Finding FB-01: Potential unauthenticated exposure of sensitive Firebase database records

**Severity:** Critical — provisional  
**Affected component:** Firebase Realtime Database root endpoint  
**Category:** Access Control / Sensitive Information Exposure

**Observation:**

The root JSON endpoint returned structured database records containing administrative credential information, device metadata, SIM information and SMS records.

**Security impact:**

If the request was unauthenticated, unauthorized parties could potentially access sensitive user information without possessing valid application credentials.

Potential consequences include:

1. Exposure of personal and device information.
2. Disclosure of mobile phone numbers and carrier details.
3. Exposure of SMS messages and potentially authentication-related content.
4. Disclosure of administrative credential material.
5. Increased risk of social engineering and targeted fraud.
6. Exposure of application management and forwarding configuration.

**Evidence:**

- `firebase_response.json`
- `firebase_response_headers.txt`
- Captured JSON excerpt.
- Recorded SHA-256 hashes.

**Verification still required:**

- Confirm HTTP status code.
- Confirm that no authentication token, session cookie or other credentials were supplied.
- Confirm that the returned records were not generated from an authenticated session.
- Determine the sensitivity and validity of the exposed credential without attempting to use it.

### Finding FB-02: Exposure of mobile device and SIM metadata

**Severity:** High — provisional  
**Category:** Privacy / Sensitive Information Disclosure

**Observation:**

Database records contained device identifiers, Android versions, manufacturer and model information, battery status, network type, carrier information and SIM phone numbers.

**Impact:**

This information can facilitate targeted profiling and social engineering and may expose the association between users, devices and mobile numbers.

### Finding FB-03: Exposure of SMS message content

**Severity:** Critical — provisional  
**Category:** Sensitive Communications Disclosure

**Observation:**

The returned JSON contained SMS message records and message content, including an excerpt that appeared to contain an OTP-related message.

**Impact:**

If accessible to unauthorized parties, SMS disclosure could expose private communications and potentially authentication-related information.

No OTP was tested or used during this investigation.

### Finding FB-04: Exposure of administrative credential material

**Severity:** Critical — provisional  
**Category:** Credential Exposure

**Observation:**

The returned JSON included a populated `password.admin_pass` field.

**Impact:**

If the credential is valid and used by an administrative component, exposure could facilitate unauthorized access to that component.

The validity, scope and privileges of the credential remain unverified.

---

## 8. Evidence Register

| Evidence ID | Evidence file | Description |
|---|---|---|
| FB-001 | `firebase_response.json` | Captured Firebase root JSON response |
| FB-002 | `firebase_response_headers.txt` | HTTP response headers |
| FB-003 | `firebase_relevant_refs.txt` | Extracted Firebase-related class references |
| FB-004 | `app_firebase_context.txt` | Application Firebase context references |
| FB-005 | `firebase_class_refs.txt` | Firebase-related class reference extraction |

### 8.1 Cryptographic hashes

**FB-001 — Firebase JSON response**

SHA-256:

`1c428c475a8b7b08c58ef9e579cf3fec8040b40b26aefb22b92d545e8b533dde`

**FB-002 — HTTP response headers**

SHA-256:

`780de1264bd19bc6f64fd23d8cf98c724f5f485e55e67c98f34fd13528db1afe`

These hashes identify the captured files at the time they were hashed. Recalculate them if the files are subsequently transferred or modified.

---

## 9. Limitations

The following limitations apply:

1. The complete HTTP status and authentication context are not included in the supplied terminal excerpt.
2. The validity and privileges of the exposed administrative credential have not been established.
3. The database project has not been independently attributed to the APK operator.
4. The complete database structure has not been exhaustively inspected.
5. The origin of every returned record has not been established.
6. No database write, modification or deletion was performed.
7. No OTP or exposed credential was used.
8. The presence of SMS or call-forwarding configuration does not establish successful execution on a victim device.
9. The CORS wildcard header is not, by itself, proof of a security vulnerability.

---

## 10. Recommended Remediation

If this database belongs to the responsible organization, the following actions are recommended:

1. Immediately restrict Realtime Database read and write permissions.
2. Require authenticated access and enforce per-user authorization.
3. Review Firebase Security Rules for every sensitive database path.
4. Remove administrative credentials and secrets from publicly readable database locations.
5. Rotate exposed credentials through the appropriate administrative process.
6. Review access logs and available audit records for unauthorized access.
7. Assess whether exposed OTPs or SMS records require incident response.
8. Minimize retention of personal and mobile-device information.
9. Separate administrative configuration from user-specific records.
10. Implement least-privilege access and periodic security-rule testing.

Do not assume that enabling Firebase Authentication alone fixes the issue; the database rules must enforce the intended authorization model.

---

## 11. Conclusion

The investigation observed a Firebase Realtime Database root endpoint returning structured JSON records containing sensitive information.

The returned sample included administrative credential material, device and SIM metadata, SMS records and forwarding-related configuration.

These observations indicate a potentially severe information-disclosure issue. If unauthenticated access is confirmed, the database should be treated as exposed and the issue escalated for immediate remediation.

The APK's static analysis independently identified SMS and call-forwarding-related functionality. However, a definitive association between the APK and the specific Firebase project remains subject to further verification.

**Final assessment:** Sensitive database information was observed in the endpoint response. Unauthenticated exposure is a high-priority finding pending confirmation of request authentication context and project attribution.

---

**Report classification:** Confidential — Digital Forensics and Malware Analysis  
**Evidence handling:** Preserve original captured files and restrict access because they contain sensitive personal and authentication-related information.