from androguard.core.dex import DEX

path = "recovery/payload_analysis/inner_apk/classes.dex"

targets = {
    "Lcom/nxtwave/berlinenxt/BootReceiver;",
    "Lcom/nxtwave/berlinenxt/CallForwardManager;",
    "Lcom/nxtwave/berlinenxt/DeviceForegroundService;",
    "Lcom/nxtwave/berlinenxt/DeviceWorker;",
    "Lcom/nxtwave/berlinenxt/SmsListenerService;",
    "Lcom/nxtwave/berlinenxt/SmsNForward;",
    "Lcom/nxtwave/berlinenxt/SmsReceiver;",
    "Lcom/nxtwave/berlinenxt/SmsSendManager;",
    "Lcom/nxtwave/berlinenxt/SmsSentReceiver;",
}

with open(path, "rb") as f:
    dex = DEX(f.read())

with open(
    "recovery/payload_analysis/priority_methods_full.txt", "w"
) as out:
    for cls in dex.get_classes():
        if cls.get_name() not in targets:
            continue

        print(f"\n{'=' * 72}\nCLASS: {cls.get_name()}", file=out)

        for method in cls.get_methods():
            print(
                f"\nMETHOD: {method.get_name()} "
                f"{method.get_descriptor()}",
                file=out,
            )

            try:
                code = method.get_code()
                if code is None:
                    print("  [no bytecode]", file=out)
                    continue

                for ins in code.get_bc().get_instructions():
                    print(
                        f"  {ins.get_name()} {ins.get_output()}",
                        file=out,
                    )

            except Exception as exc:
                print(
                    f"  [decode error: {type(exc).__name__}: {exc}]",
                    file=out,
                )

print("Report written to recovery/payload_analysis/priority_methods_full.txt")