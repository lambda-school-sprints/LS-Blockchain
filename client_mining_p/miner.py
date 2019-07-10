import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 
def proof_is_valid(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash.startswith('000000')


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    proof = 0
    while not proof_is_valid(last_proof, proof):
        proof += 1

    return proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        response = requests.get(f'{node}/last-proof').json()
        last_proof = response['proof']
        new_proof = proof_of_work(last_proof)
        # TODO: When found, POST it to the server {"proof": new_proof}
        response = requests.post(
            f'{node}/mine', json={"proof": new_proof}).json()

        # TODO: If the server responds with 'New Block Forged'
        if response['message'] == 'New Block Forged':
            coins_mined += 1
            print(f'{coins_mined} coins mined')
        else:
            print(f'Error: {response}')
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
