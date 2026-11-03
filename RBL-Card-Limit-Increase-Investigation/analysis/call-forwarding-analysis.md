# Call Forwarding Analysis — RBL-Themed Android APK

**Investigation:** RBL Card Limit Increase APK  
**Analysis type:** Static analysis  
**Component:** Android call-forwarding service  
**Status:** Static-analysis phase completed; runtime behavior not verified

---

## 1. Executive Summary

Static analysis of the APK's recovered DEX code identified a dedicated Android service named `CallForwardManager`, which implements a remotely controlled call-forwarding workflow.

The service reads command data associated with a Firebase Realtime Database path, extracts a forwarding destination number, SIM slot, action, and command status, and processes eligible commands.

The activation path constructs a GSM USSD string in the following format:

```text
*21*<destination_number>#
```

The application attempts to submit this request through Android's `TelephonyManager.sendUssdRequest()` API. An Intent-based fallback is also present.

These findings establish that the APK contains code designed to request unconditional call forwarding to a dynamically supplied destination number. However, static analysis alone does not establish that the network accepted the request or that call forwarding was successfully activated on a device.

## 2. Investigation Scope

The investigation focused on:

- Identifying the call-forwarding service.
- Understanding how remote commands are retrieved and processed.
- Identifying command fields and status checks.
- Reconstructing the activation USSD string.
- Examining SIM selection and USSD execution.
- Identifying the deactivation path and remaining uncertainties.

The analysis was performed against the recovered DEX code using JADX and Androguard-based instruction extraction.

## 3. Relevant Components

| Component | Observed role |
|---|---|
| `com.nxtwave.berlinenxt.CallForwardManager` | Android service coordinating call-forwarding commands |
| `Ly0/m` | SIM-specific TelephonyManager and USSD helper |
| `Li2/b` | Runnable containing the activation USSD construction |
| `Li2/k` | Call-forwarding execution-related class |
| `Ly0/c` | Handler dispatched by the stop-command branch |
| `TelephonyManager.UssdResponseCallback` subclass | USSD response callback implementation |

Some class and method names are obfuscated. Their roles above are based on observed references and instruction behavior, not assumed source-code names.

## 4. Remote Command Architecture

The service references the following Firebase database path:

```text
users/{device_id}/call_forward/{value}
```

The command-processing method reads these fields:

| Field | Observed purpose |
|---|---|
| `forward_number` | Destination number for forwarding |
| `sim_slot` | SIM selection value |
| `action` | Requested operation |
| `status` | Command-processing state |

The service logs the extracted command values and evaluates the command status.

### Command processing

The extracted instructions show:

1. The command data is read.
2. `forward_number`, `sim_slot`, `action`, and `status` are extracted.
3. A command with status `pending` is eligible for further processing.
4. A missing forwarding number results in a failure status.
5. A command with status `stop` follows a separate handler branch.
6. The `deactivate` action is checked in the execution flow.

The exact Firebase command producer and the complete backend-side workflow were not established in this analysis.

## 5. Call-Forwarding Activation

The activation runnable `Li2/b.run()` contains the following string constant:

```java
const-string v0, "*21*"
```

It also constructs a log message:

```text
Activating call forwarding to <destination_number> on SIM <sim_slot>
```

The destination number is appended dynamically.

The caller constructs the final request by appending `#` to the generated string and passes it to the SIM-specific USSD helper.

### Reconstructed request

```text
*21*<destination_number>#
```

This is the GSM unconditional call-forwarding activation format.

**Forensic interpretation:** The application contains code designed to request unconditional call forwarding to a destination supplied through the command data.

## 6. USSD Execution Mechanism

The helper method identified as:

```text
Ly0/m.G(
    TelephonyManager,
    String
): boolean
```

contains the following behavior:

- Checks the Android SDK version.
- For Android SDK 26 and above, retrieves `sendUssdRequest` using Java reflection.
- Creates a USSD response callback object.
- Supplies a Handler.
- Invokes the reflected method with the provided USSD string.
- Logs an error if invocation fails.

The code also contains a lower-level TelephonyManager acquisition path and an Intent-based fallback.

The surrounding helper checks the `CALL_PHONE` permission before proceeding with the request workflow.

**Important distinction:** The log message `USSD sent successfully via TelephonyManager` represents an application-side success path. It does not independently prove successful execution by the mobile network.

## 7. SIM Selection

The helper method `Ly0/m.F(I, String)` obtains a `TelephonyManager` associated with a selected SIM slot.

The extracted instructions show that:

- The SIM slot is supplied as an integer.
- A SIM-specific TelephonyManager is obtained.
- The USSD string is passed to `Ly0/m.G()`.
- The helper returns a boolean indicating its execution path result.

The precise mapping between the application's SIM slot value and the physical SIM configuration was not verified on a device.

## 8. Deactivation and Stop Handling

The command-processing method checks for an action value of:

```text
deactivate
```

A separate branch handles a command whose status is:

```text
stop
```

The stop branch creates a `Ly0/c` object and schedules it through an executor.

The available extracted instructions do not establish the exact deactivation USSD string or conclusively show the complete behavior of the `Ly0/c` handler.

Therefore, the presence of a deactivation-related code path is confirmed, but successful deactivation is not established.

## 9. Evidence Summary

| Finding | Assessment |
|---|---|
| Dedicated `CallForwardManager` service | Confirmed |
| Firebase call-forwarding command path | Confirmed |
| Remote destination number field | Confirmed |
| SIM slot field | Confirmed |
| Action and status fields | Confirmed |
| Pending-command processing | Confirmed |
| Missing-number validation | Confirmed |
| Activation string construction | Confirmed |
| `TelephonyManager.sendUssdRequest()` invocation | Confirmed |
| Intent-based fallback | Confirmed |
| Deactivation-related branch | Confirmed |
| Exact deactivation request | Not established |
| Successful network-side activation | Not verified |
| Successful network-side deactivation | Not verified |

## 10. Limitations

This investigation was based on static inspection of recovered DEX instructions.

The following were not established:

- Whether the application successfully activated call forwarding on a real device.
- Whether the mobile operator accepted or rejected the USSD request.
- The actual destination number used in a real command.
- The complete behavior of the stop handler.
- The exact deactivation USSD string.
- Whether the Firebase command workflow was operational during the investigation.

No live call-forwarding request was issued as part of this static-analysis work.

## 11. Security Significance

The combination of remote command fields, a dynamically supplied forwarding destination, SIM selection, and USSD request execution represents a significant security concern.

If an attacker can control the relevant command records and the application processes those commands on a victim's device, the implementation could be abused to request unconditional call forwarding to an attacker-controlled number.

Potential consequences include:

- Redirection of incoming calls.
- Interception of voice-based verification calls.
- Disruption of normal incoming-call delivery.
- Abuse of remotely controlled device functionality.

These are potential impacts inferred from the identified implementation. Actual exploitation, backend access, and successful network-side activation were not demonstrated.

## 12. Conclusion

Static analysis identified a dedicated, Firebase-connected call-forwarding implementation within the investigated APK.

The application extracts a forwarding destination and SIM selection from remote command data, constructs an unconditional call-forwarding USSD request in the format:

```text
*21*<destination_number>#
```

It then attempts to submit the request through Android's TelephonyManager USSD API, with an alternative Intent-based execution path.

This establishes the presence of a remotely controlled call-forwarding capability in the APK's code. It does not establish that call forwarding was successfully activated on any device.

**Final assessment:** Call-forwarding activation logic identified through static analysis. Runtime and network-side effects remain unverified.
