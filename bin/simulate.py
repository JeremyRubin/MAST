
first = Mast("""
if (signed(frank, signature)):
    # Allow alice to pass in a new txn, not hard coded(ContractTxn)
    return Valid([args[-1]])
""")


will = Mast("""
if (signed(alice, signature)):
    # Allow alice to pass in a new txn, not hard coded(ContractTxn)
    return Valid([args[-1]])
if (signed([bob and carol], signature)):
    if (args[1] > 3 and args[1] < 10):
        return Valid(["output txn doing something specific"])
    #? more conditions
if (date.time.now() > year100000)
    return ?
""")


mWill = Mast(prelude)
map(mWill.addBr,
["""
if (signed(alice, signature)):
    # Allow alice to pass in a new txn, not hard coded(ContractTxn)
    return Valid([args[-1]])
""",
"""
if (signed([bob and carol], signature)):
    if (args[1] > 3 and args[1] < 10):
        return Valid(["output txn doing something specific"])
    #? more conditions
""",
"""
if (date.time.now() > year100000)
    return ?
"""])


if __name__ == "__main__":
    #initialize
    consent_tick()
    hash = ?
    arglist = ?
    [node.recv(hash, arglist) for node in nodes]
    consent_tick()
