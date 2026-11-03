from androguard.core.dex import DEX
from pathlib import Path
import hashlib
import traceback

dex_path = Path("inner_apk/classes.dex")

data = dex_path.read_bytes()

print("[+] File:", dex_path)
print("[+] Size:", len(data))
print("[+] SHA256:", hashlib.sha256(data).hexdigest())

try:
    dex = DEX(data)
    print("\n[+] Androguard successfully parsed DEX")

    targets = [
        "Lcom/nxtwave/berlinenxt/CallForwardManager;",
        "Li2/C0266e;",
        "Ly0/m;",
    ]

    for target in targets:
        print(f"\n{'=' * 65}")
        print("[TARGET]", target)

        classes = [
            c for c in dex.get_classes()
            if c.get_name() == target
        ]

        if not classes:
            print("[-] Class not found")
            continue

        for cls in classes:
            print("[+] Class:", cls.get_name())

            for method in cls.get_methods():
                print(
                    "  Method:",
                    method.get_name(),
                    method.get_descriptor()
                )

                try:
                    code = method.get_code()
                    if code is None:
                        print("    [No code]")
                    else:
                        print("    Registers:", code.get_registers_size())
                        print("    Instructions:", code.get_insns_size())
                except Exception as exc:
                    print("    [Instruction inspection error]", repr(exc))

except Exception:
    print("\n[!] Androguard parsing failed")
    traceback.print_exc()