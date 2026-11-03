# APK Static Analysis — RBL Card Limit Increase

## 1. Investigation Objective

This report documents the initial static examination of an Android application named **RBL CARD LIMIT UPDATE**. The objective is to establish the APK's identity, preserve its cryptographic identifiers, record its file metadata, and document notable observations from its archive listing.

This is an initial APK-level assessment. It does not, by itself, establish the application's runtime behaviour or malicious classification.

## 2. Evidence Identification

| Attribute | Observed value |
|---|---|
| Original filename | `RBL CARD LIMIT UPDATE.apk` |
| Evidence location | `original/RBL CARD LIMIT UPDATE.apk` |
| File format | Android application package (APK) |
| File size | 6,550,646 bytes |
| SHA-256 | `5f1f6e699667955bdcf8524170af48d1a1f50f3cc1d844ba4dd4daa830d7083b` |
| MD5 | `38b3f62a10311f72401a96ac85122c11` |
| Filesystem modification time | 2026-10-13 05:35:41.851 (reported timezone: UTC−04:00) |

A second file named `RBL CARD LIMIT UPDATE (copy 1).apk` was also identified. Both APK copies were reported to have the same size and SHA-256 hash.

The matching hashes indicate that the two files are byte-identical with respect to the SHA-256 comparison. Both original files should be retained as evidence.

## 3. Evidence Integrity

The SHA-256 digest is the primary integrity identifier used in this investigation.

The MD5 digest is retained as a supplementary legacy identifier, not as the primary integrity mechanism.

The recorded hashes can be used to verify that subsequent working copies match the original evidence.

## 4. Archive Structure Observations

The supplied APK archive listing contains entries associated with conventional Android application components, including:

- `AndroidManifest.xml`
- `resources.arsc`
- `classes.dex`
- `META-INF/`
- `res/`
- `kotlin/`

The listing also contains unusual archive entry names, including repeated forward slashes, backslashes, leading slashes, and extensions that do not correspond to the apparent underlying Android component.

Examples include entries resembling:

- `AndroidManifest.xml/..xml`
- `/AndroidManifest.xml///.xml`
- `classes.dex/\\\\.xml`
- `kotlin/collections/classes.dex.xml`

These observations warrant further examination of the APK's ZIP entry names and archive structure.

**Important:** The listing alone does not establish whether these entries are malformed, deliberately crafted, or capable of exploiting a particular extraction tool. Additional validation is required.

## 5. Preliminary Assessment

The initial examination establishes:

1. The evidence is an APK file with a recorded size of 6,550,646 bytes.
2. Two collected APK copies have matching SHA-256 hashes.
3. The archive listing contains conventional Android package components.
4. The archive listing also contains unusual entry names that require further validation.

No malware-family attribution or confirmed malicious behaviour is established by this report.

## 6. Limitations

This report is limited to the supplied filesystem metadata, cryptographic hashes, and archive listing.

It does not establish:

- Whether the application successfully installs or executes.
- Whether the application communicates with a malicious backend.
- Whether SMS, telephony, or other sensitive operations were executed.
- Whether any extracted payload is malicious.
- Whether the unusual archive entries exploit a vulnerability.

These questions require supporting analysis of the manifest, DEX code, embedded payloads, configuration data, and runtime evidence where available.

## 7. Next Investigation Areas

The next reports will examine:

1. Android manifest and application permissions.
2. Embedded payload and secondary APK analysis.
3. SMS-related implementation paths.
4. Firebase configuration and code references.
5. Telephony and call-forwarding references.
6. WebView implementation.
7. VPN-related code references.

Each finding will be linked to its supporting evidence and assigned an appropriate confidence level.

## 8. Evidence Handling Note

Original APK files must remain preserved. Analysis should be performed on verified working copies.

Raw APKs, extracted DEX files, private configuration files, credentials, and unsanitized logs must not be included in the public GitHub repository.