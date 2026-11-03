# Android Manifest Analysis — RBL Card Limit Increase

## 1. Objective

This report documents the manifest-related findings obtained during the static investigation of the Android application presenting itself as **RBL CARD LIMIT INCREASE**.

The examination focuses on application identity, SDK configuration, requested permissions, and security-relevant capabilities.

The outer application and its embedded payload are treated as separate artifacts throughout this investigation.

## 2. Outer Application Identification

| Attribute | Observed value |
|---|---|
| Application label | RBL CARD LIMIT INCREASE |
| Package name | `com.rblcard_jagtd` |
| Version code | 1 |
| Version name | 1.0 |
| Minimum SDK | 25 |
| Target SDK | 34 |
| Compile SDK | 35 |
| Platform build version | 15 |

The application presents itself as an RBL Card Limit Increase application. Its branding does not independently establish an official relationship with RBL Bank.

## 3. Requested Permissions

The extracted application metadata identifies the following permissions:

| Permission | Security relevance |
|---|---|
| `INTERNET` | Network communication |
| `READ_PHONE_STATE` | Access to certain telephony and device-state information |
| `READ_PHONE_NUMBERS` | Access to phone-number information |
| `ACCESS_NETWORK_STATE` | Network connectivity inspection |
| `FOREGROUND_SERVICE` | Foreground service execution |
| `FOREGROUND_SERVICE_DATA_SYNC` | Data-sync foreground service declaration |
| `POST_NOTIFICATIONS` | Notification delivery |
| `WAKE_LOCK` | Device wake-state management |
| `RECEIVE_SMS` | SMS broadcast reception |
| `READ_SMS` | SMS data access |
| `SEND_SMS` | SMS transmission |
| `RECEIVE_MMS` | MMS-related broadcast reception |
| `CALL_PHONE` | Initiating phone calls |
| `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` | Requesting battery optimization exemption |
| `SCHEDULE_EXACT_ALARM` | Scheduling exact alarms |
| `USE_EXACT_ALARM` | Exact alarm capability |
| `RECEIVE_BOOT_COMPLETED` | Receiving device boot notification |

These are declared capabilities. Their presence does not establish that the application successfully exercised them.

## 4. Security-Relevant Permission Analysis

### 4.1 SMS capabilities

The application requests:

- `READ_SMS`
- `RECEIVE_SMS`
- `SEND_SMS`
- `RECEIVE_MMS`

These permissions warrant examination because they relate to user communications and messaging data.

Separate static DEX evidence from the investigation identifies an SMS-sending implementation that checks `SEND_SMS` permission and references Android APIs including:

- `SmsManager.sendTextMessage()`
- `SmsManager.divideMessage()`
- `SmsManager.sendMultipartTextMessage()`

This supports the existence of an SMS-sending code path. It does not prove successful message delivery or runtime execution.

### 4.2 Telephony capabilities

The application requests:

- `READ_PHONE_STATE`
- `READ_PHONE_NUMBERS`
- `CALL_PHONE`

These permissions warrant further examination of telephony-related implementation paths.

The actual use of call-forwarding functionality must be established separately through code analysis.

### 4.3 Network capabilities

The application requests:

- `INTERNET`
- `ACCESS_NETWORK_STATE`

These permissions support network communication and connectivity inspection.

Further investigation is necessary to establish the actual backend destinations and data exchanged.

### 4.4 Background execution

The application requests:

- `FOREGROUND_SERVICE`
- `FOREGROUND_SERVICE_DATA_SYNC`
- `WAKE_LOCK`
- `RECEIVE_BOOT_COMPLETED`
- `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`

These declarations warrant examination of background services, boot receivers, and application lifecycle behaviour.

They do not independently establish persistence or continuous background execution.

### 4.5 Alarm scheduling

The application requests:

- `SCHEDULE_EXACT_ALARM`
- `USE_EXACT_ALARM`

These declarations relate to exact alarm scheduling. The purpose and implementation of scheduled tasks remain subject to further analysis.

## 5. Embedded Payload — Separate Manifest Findings

The investigation also identified an embedded APK under:

`recovery/payload_analysis/inner_apk/`

Its extracted manifest is an Android Binary XML file.

String data recovered from this binary manifest identifies the following component class names under the package:

`com.nxtwave.berlinenxt`

| Component | Class name |
|---|---|
| Main activity | `MainActivity` |
| SMS service | `SmsListenerService` |
| SMS receiver | `SmsReceiver` |
| SMS-related class | `SmsNForward` |
| SMS service | `SmsSendManager` |
| Telephony service | `CallForwardManager` |
| Boot receiver | `BootReceiver` |
| Foreground service | `DeviceForegroundService` |
| Application class | `MyApp` |

These names are observations from the embedded payload's binary manifest data. The complete declarations, attributes, exported status, and intent filters have not yet been independently decoded and validated.

These components must not be attributed to the outer application's manifest without further evidence.

## 6. Manifest Extraction Limitations

The original outer manifest was identified as Android Binary XML.

The existing `recovery/manifest/manifest_xmltree.txt` contains the following extraction errors:

- `Unknown chunk type 0x0 in table at 0xc`
- `BAD DEPTH in XMLBlock: -1`

The inner payload manifest was also identified as Android Binary XML.

The expected APKTool-decoded outer manifest was not found at:

`recovery/apktool_decoded/AndroidManifest.xml`

The JADX manifest output at:

`static/jadx_out/resources/AndroidManifest.xml`

contains only 39 bytes and does not provide a usable decoded manifest.

Additionally, JADX-generated source files contain multiple method decompilation errors, limiting the reliability of some reconstructed Java methods.

A separate manifest decoding and validation step is therefore required before publishing a complete component inventory.

## 7. Assessment

The outer application's extracted metadata establishes a combination of sensitive requested capabilities involving SMS, telephony, network access, and background execution.

The embedded payload's binary manifest data exposes component names associated with SMS handling, SMS sending, call forwarding, boot events, and foreground services.

These observations justify deeper investigation of the embedded payload.

However, manifest declarations and component names alone do not establish successful execution, malicious intent, or actual compromise.

## 8. Next Investigation Steps

1. Decode and validate the outer APK manifest.
2. Decode and validate the embedded payload manifest.
3. Examine exported component declarations and intent filters.
4. Correlate SMS components with DEX implementation paths.
5. Examine call-forwarding implementation and relevant telephony APIs.
6. Examine boot receiver and foreground-service behaviour.
7. Preserve the extraction logs and document tool limitations.

## 9. Conclusion

The manifest-related evidence identifies sensitive messaging and telephony capabilities in the outer application and additional SMS- and telephony-associated component names in the embedded payload.

The distinction between the two application packages is important to maintaining an accurate evidence record.

Further manifest decoding and code-path validation are necessary before making stronger behavioural or maliciousness claims.