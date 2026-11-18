from random import choices, uniform, randint

from flask import Flask, jsonify, render_template


app = Flask(__name__)


# ---------------------------------------------------------
# CS:GO Weapon Case
#
# weight = chance used when selecting the winning item.
# min_float / max_float = valid wear range for that skin.
# ---------------------------------------------------------

ITEMS = [
    # Mil-Spec Grade
    {
        "name": "MP7 | Skulls",
        "rarity": "Mil-Spec",
        "color": "#4b69ff",
        "weight": 26.64,
        "min_float": 0.10,
        "max_float": 0.26,
    },
    {
        "name": "AUG | Wings",
        "rarity": "Mil-Spec",
        "color": "#4b69ff",
        "weight": 26.64,
        "min_float": 0.00,
        "max_float": 0.14,
    },
    {
        "name": "SG 553 | Ultraviolet",
        "rarity": "Mil-Spec",
        "color": "#4b69ff",
        "weight": 26.64,
        "min_float": 0.06,
        "max_float": 0.80,
    },

    # Restricted
    {
        "name": "Glock-18 | Dragon Tattoo",
        "rarity": "Restricted",
        "color": "#8847ff",
        "weight": 5.3267,
        "min_float": 0.00,
        "max_float": 0.08,
    },
    {
        "name": "USP-S | Dark Water",
        "rarity": "Restricted",
        "color": "#8847ff",
        "weight": 5.3267,
        "min_float": 0.10,
        "max_float": 0.26,
    },
    {
        "name": "M4A1-S | Dark Water",
        "rarity": "Restricted",
        "color": "#8847ff",
        "weight": 5.3266,
        "min_float": 0.10,
        "max_float": 0.26,
    },

    # Classified
    {
        "name": "AK-47 | Case Hardened",
        "rarity": "Classified",
        "color": "#d32ce6",
        "weight": 1.60,
        "min_float": 0.00,
        "max_float": 1.00,
    },
    {
        "name": "Desert Eagle | Hypnotic",
        "rarity": "Classified",
        "color": "#d32ce6",
        "weight": 1.60,
        "min_float": 0.00,
        "max_float": 0.08,
    },

    # Covert
    {
        "name": "AWP | Lightning Strike",
        "rarity": "Covert",
        "color": "#eb4b4b",
        "weight": 0.64,
        "min_float": 0.00,
        "max_float": 0.08,
    },

    # Rare Special Item
    {
        "name": "★ Rare Special Item",
        "rarity": "Special",
        "color": "#ffd700",
        "weight": 0.26,
        "min_float": 0.00,
        "max_float": 1.00,
    },
]


# ---------------------------------------------------------
# Float / wear functions
# ---------------------------------------------------------

def random_float(min_float, max_float):
    """Generate a random float inside the skin's valid range."""

    return round(
        uniform(min_float, max_float),
        8,
    )


def wear_name(value):
    """Convert a float value into a CS wear condition."""

    if value < 0.07:
        return "Factory New"

    if value < 0.15:
        return "Minimal Wear"

    if value < 0.38:
        return "Field-Tested"

    if value < 0.45:
        return "Well-Worn"

    return "Battle-Scarred"


# ---------------------------------------------------------
# Pages
# ---------------------------------------------------------

@app.get("/")
def home():
    return render_template(
        "index.html",
        items=ITEMS,
    )


# ---------------------------------------------------------
# API
# ---------------------------------------------------------

@app.post("/api/open")
def open_case():

    # Choose the winning skin using its drop weight.
    item = choices(
        ITEMS,
        weights=[item["weight"] for item in ITEMS],
        k=1,
    )[0].copy()

    # Generate a float that is valid for THIS skin.
    float_value = random_float(
        item["min_float"],
        item["max_float"],
    )

    # Add generated information to the result.
    item["float"] = float_value
    item["wear"] = wear_name(float_value)

    # Paint seed / pattern ID.
    item["seed"] = randint(1, 1000)

    return jsonify(item)


# ---------------------------------------------------------
# Start Flask
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)