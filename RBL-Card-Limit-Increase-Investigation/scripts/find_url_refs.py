from androguard.core.apk import APK
from androguard.core.dex import DEX

apk_path = "recovery/payload_analysis/payload.decrypted"
target = "https://z.devalphas.online/sb/rb3/fx/"

with open(apk_path, "rb") as f:
    apk = APK(apk_path)

dex = DEX(apk.get_dex())

matches = []
for s in dex.get_strings():
    if target in s:
        matches.append(s)

print("Matching DEX strings:")
for s in matches:
    print(repr(s))

print("\nSearching encoded methods for references...")
found = False

for cls in dex.get_classes():
    for method in cls.get_methods():
        code = method.get_code()
        if code is None:
            continue
        for ins in code.get_bc().get_instructions():
            output = ins.get_output()
            if target in output:
                found = True
                print(
                    "CLASS:", cls.get_name(),
                    "METHOD:", method.get_name(),
                    "DESC:", method.get_descriptor(),
                    "INSTRUCTION:", ins.get_name(),
                    "OUTPUT:", output
                )

if not found:
    print("No direct instruction reference found.")
    print("The string may be referenced indirectly or stored in a string table.")