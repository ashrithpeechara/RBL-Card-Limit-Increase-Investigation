from androguard.core.dex import DEX

path = "recovery/payload_analysis/inner_apk/classes.dex"

targets = {
    "Lcom/nxtwave/berlinenxt/CallForwardManager;",
    "Lcom/nxtwave/berlinenxt/SmsNForward;",
    "Lcom/nxtwave/berlinenxt/SmsSendManager;",
    "Lcom/nxtwave/berlinenxt/SmsListenerService;",
    "Lcom/nxtwave/berlinenxt/SmsReceiver;",
    "Lcom/nxtwave/berlinenxt/SmsSentReceiver;",
    "Lcom/nxtwave/berlinenxt/BootReceiver;",
    "Lcom/nxtwave/berlinenxt/DeviceForegroundService;",
    "Lcom/nxtwave/berlinenxt/DeviceWorker;",
}

needles = (
    "SmsManager", "TelephonyManager", "sendUssdRequest",
    "sendTextMessage", "sendMultipartTextMessage",
    "getLine1Number", "getDeviceId", "getSubscriberId",
    "getSimSerialNumber", "HttpURLConnection", "Firebase",
    "BOOT_COMPLETED", "SMS_RECEIVED", "https://", "http://",
)

with open(path, "rb") as f:
    dex = DEX(f.read())

found = set()

for cls in dex.get_classes():
    name = cls.get_name()
    if name not in targets:
        continue

    found.add(name)
    print(f"\n{'=' * 72}\nCLASS: {name}")
    for method in cls.get_methods():
        print(f"\nMETHOD: {method.get_name()} {method.get_descriptor()}")
        try:
            code = method.get_code()
            if code is None:
                print("  [no code: abstract/native or unavailable]")
                continue

            for ins in code.get_bc().get_instructions():
                output = f"  {ins.get_name()} {ins.get_output()}"
                if any(x.lower() in output.lower() for x in needles):
                    print(output)
        except Exception as exc:
            print("  [instruction decoding error]", repr(exc))

print("\n\nTARGET CLASS SUMMARY")
for name in sorted(targets):
    print(("FOUND " if name in found else "NOT ENUMERATED ") + name)