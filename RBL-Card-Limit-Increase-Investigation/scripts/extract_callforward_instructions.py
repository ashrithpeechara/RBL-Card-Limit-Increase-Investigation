from androguard.core.dex import DEX
from pathlib import Path

dex = DEX(Path("inner_apk/classes.dex").read_bytes())

output = Path("callforward_recovery")
output.mkdir(exist_ok=True)

report = []

def dump_class(cls, selected_methods=None):
    report.append("\n" + "=" * 80)
    report.append("CLASS: " + cls.get_name())
    report.append("SUPERCLASS: " + str(cls.get_superclassname()))

    for method in cls.get_methods():
        name = method.get_name()
        descriptor = method.get_descriptor()

        if selected_methods is not None:
            if (name, descriptor) not in selected_methods:
                continue

        report.append(f"\nMETHOD: {name} {descriptor}")

        code = method.get_code()
        if code is None:
            report.append("[No method code]")
            continue

        try:
            instructions = code.get_bc().get_instructions()

            for index, ins in enumerate(instructions):
                report.append(
                    f"{index:04d}  {ins.get_name()}  {ins.get_output()}"
                )

        except Exception as exc:
            report.append("[Instruction decoding error] " + repr(exc))

# 1. CallForwardManager: inspect all methods
for cls in dex.get_classes():
    if cls.get_name() == "Lcom/nxtwave/berlinenxt/CallForwardManager;":
        dump_class(cls)

# 2. Potential USSD execution method
for cls in dex.get_classes():
    if cls.get_name() == "Ly0/m;":
        dump_class(
            cls,
            {
                (
                    "G",
                    "(Landroid/telephony/TelephonyManager;"
                    "Ljava/lang/String;)Z"
                )
            }
        )

# 3. Find USSD response callback by superclass
callback_super = (
    "Landroid/telephony/TelephonyManager$UssdResponseCallback;"
)

for cls in dex.get_classes():
    if cls.get_superclassname() == callback_super:
        dump_class(cls)

report_path = output / "androguard_callforward_instructions.txt"
report_path.write_text("\n".join(report), encoding="utf-8")

print("[+] Extraction completed")
print("[+] Output:", report_path)
print("[+] Lines:", len(report))
print("[+] Callback classes and target methods inspected")