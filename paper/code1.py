ex = "some code"
M = Mast("compile", "")
n = M
for i, c in enumerate(X*[code]):
    [n.addBr(c) for i in xrange(Y)]
    n = n.addBr(c)
proof = n.generateFullProofUpward(M.hash)
# Run in simulator
merkleVerifyExec(M.hash(), proof, 10)
# Generate and run as Bitcoin script
scriptSig, script = toScript(pr, M.hash)
full = scriptSig + script
run(full)
print "compression rate:", 1-len(together)/(len(code)*(Y+1))
