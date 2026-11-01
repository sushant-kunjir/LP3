
from flask import Flask, render_template, request, redirect, url_for
import hashlib
import json
from datetime import datetime

app = Flask(__name__)


# ---------------- BLOCK CLASS ----------------

class Block:

    def __init__(self, index, data, previous_hash):

        self.index = index
        self.timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.data = data
        self.previous_hash = previous_hash

        self.hash = self.calculate_hash()

    # Generate SHA-256 hash
    def calculate_hash(self):

        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }

        encoded = json.dumps(
            block_data,
            sort_keys=True
        ).encode()

        return hashlib.sha256(encoded).hexdigest()


# ---------------- BLOCKCHAIN CLASS ----------------

class MentalHealthBlockchain:

    def __init__(self):

        # Create Genesis Block
        self.chain = [
            Block(
                0,
                {"message": "Genesis Block"},
                "0"
            )
        ]

    # Add new mental health record
    def add_record(self, mood, note):

        previous_block = self.chain[-1]

        data = {
            "mood": mood,
            "note": note
        }

        block = Block(
            len(self.chain),
            data,
            previous_block.hash
        )

        self.chain.append(block)

    # Verify blockchain integrity
    def verify_chain(self):

        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verify current block hash
            if current.hash != current.calculate_hash():
                return False

            # Verify previous block connection
            if current.previous_hash != previous.hash:
                return False

        return True


# ---------------- CREATE BLOCKCHAIN ----------------

blockchain = MentalHealthBlockchain()


# ---------------- HOME ROUTE ----------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        mood = request.form.get(
            "mood", ""
        ).strip()

        note = request.form.get(
            "note", ""
        ).strip()

        if mood and note:

            blockchain.add_record(
                mood,
                note
            )

            return redirect(url_for("home"))

    return render_template(
        "index.html",
        records=blockchain.chain[1:],
        verified=blockchain.verify_chain(),
        total=len(blockchain.chain) - 1
    )


# ---------------- BLOCKCHAIN DETAILS ROUTE ----------------

@app.route("/blockchain")
def blockchain_details():

    return render_template(
        "blockchain.html",
        chain=blockchain.chain,
        verified=blockchain.verify_chain()
    )


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )
