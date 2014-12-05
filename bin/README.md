Contracts
---------

Protocol
We will define the protocol of a contract using the mast as follows:

Two parties, A and B, where:
A- the creator of the contract
B- the signer of the contract

A drafts a contract requesting the signature of B and sends the contract to B

B then sequentially executes aspects of this contract, with alternate paths closed off upon divergence(for example, the else clause of a fulfilled if/else statement)

A verifies the capability of B to execute each branch(in the case of multiparty signing, all parties may not have access to the same components of the contract). Once a branch has been executed, traversal down alternate paths is disallowed, though loops through a previously executed portion of the tree is allowed