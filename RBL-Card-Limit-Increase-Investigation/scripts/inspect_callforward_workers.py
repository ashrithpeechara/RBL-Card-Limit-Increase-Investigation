from androguard.core.dex import DEX
from pathlib import Path

dex = DEX(Path("inner_apk/classes.dex").read_bytes())

targets = {
    "Lcom/nxtwave/berlinenxt/CallForwardManager;",
    "Li2/k;",
    "Li2/b;",
    "Ly0/c;",
    "Li2/e;",
    "Ly0/m;",
}

out = []

for cls in dex.get_classes():
    if cls.get_name() not in targets:
        continue

    out.append("\n" + "=" * 90)
    out.append("CLASS: " + cls.get_name())
    out.append("SUPERCLASS: " + str(cls.get_superclassname()))

    for method in cls.get_methods():
        out.append(
            f"\nMETHOD: {method.get_name()} {method.get_descriptor()}"
        )

        code = method.get_code()
        if code is None:
            out.append("[No method code]")
            continue

        try:
            for i, ins in enumerate(code.get_bc().get_instructions()):
                out.append(
                    f"{i:04d} {ins.get_name()} {ins.get_output()}"
                )
        except Exception as e:
            out.append("[Decode error] " + repr(e))

# Search every class for actual USSD API references
out.append("\n" + "=" * 90)
out.append("GLOBAL USSD API REFERENCE SEARCH")

for cls in dex.get_classes():
    for method in cls.get_methods():
        code = method.get_code()
        if code is None:
            continue

        try:
            for i, ins in enumerate(code.get_bc().get_instructions()):
                text = ins.get_output()
                if any(x.lower() in text.lower() for x in [
                    "sendUssdRequest",
                    "UssdResponseCallback",
                    "TelephonyManager",
                    "callForward"
                ]):
                    out.append(
                        f"{cls.get_name()} -> "
                        f"{method.get_name()} {method.get_descriptor()}"
                    )
                    out.append(f"  {i:04d} {ins.get_name()} {text}")
        except Exception:
            pass

path = Path("callforward_recovery/callforward_worker_analysis.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("\n".join(out), encoding="utf-8")

print("[+] Analysis written to:", path)
print("[+] Lines:", len(out))