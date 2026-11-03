from androguard.core.dex import DEX

path = "recovery/payload_analysis/inner_apk/classes.dex"

with open(path, "rb") as f:
    dex = DEX(f.read())

classes = list(dex.get_classes())
print("Total classes enumerated:", len(classes))

for cls in classes:
    name = cls.get_name()
    if any(token in name for token in ("Li2", "Ly0", "SmsSendManager")):
        print(name)