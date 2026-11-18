const track = document.querySelector("#track");
const openButton = document.querySelector("#openButton");
const result = document.querySelector("#result");
const reel = document.querySelector(".reel-shell");
const items = window.CASE_ITEMS;

const WINNER_INDEX = 46;
const REEL_SIZE = 54;
const GAP = 8;

function randomItem() {
  return items[Math.floor(Math.random() * items.length)];
}

function createCard(item) {
  const card = document.createElement("div");
  card.className = "roll-card";
  card.style.setProperty("--rarity", item.color);
  card.textContent = item.name;
  return card;
}

function buildReel(winner) {
  const reelItems = Array.from({ length: REEL_SIZE }, randomItem);
  reelItems[WINNER_INDEX] = winner;
  track.replaceChildren(...reelItems.map(createCard));
}

async function requestWinner() {
  const response = await fetch("/api/open", { method: "POST" });
  if (!response.ok) throw new Error("The Flask API returned an error.");
  return response.json();
}

function animateToWinner() {
  const cardWidth = track.children[0].getBoundingClientRect().width;
  const winnerCenter = WINNER_INDEX * (cardWidth + GAP) + cardWidth / 2;
  const target = winnerCenter - reel.clientWidth / 2;

  track.style.transition = "none";
  track.style.transform = "translateX(0)";

  requestAnimationFrame(() => requestAnimationFrame(() => {
    track.style.transition = "transform 6.2s cubic-bezier(.08,.66,.16,1)";
    track.style.transform = `translateX(-${target}px)`;
  }));
}

async function openCase() {
  openButton.disabled = true;
  result.textContent = "Opening...";

  try {
    const winner = await requestWinner();
    buildReel(winner);
    animateToWinner();

    window.setTimeout(() => {

      // Show short result next to the OPEN CASE button
      result.textContent = `You unboxed ${winner.name}`;

      // Get the winner panel elements
      const winnerPanel =
        document.querySelector("#winnerPanel");

      const winnerName =
        document.querySelector("#winnerName");

      const winnerRarity =
        document.querySelector("#winnerRarity");

      const winnerFloat =
        document.querySelector("#winnerFloat");

      const winnerWear =
        document.querySelector("#winnerWear");

      const winnerSeed =
        document.querySelector("#winnerSeed");

      // Add the generated Flask values
      winnerName.textContent =
        winner.name;

      winnerRarity.textContent =
        winner.rarity;

      winnerFloat.textContent =
        Number(winner.float).toFixed(8);

      winnerWear.textContent =
        winner.wear;

      winnerSeed.textContent =
        winner.seed;


      // Use the rarity colour for the result
      winnerPanel.style.setProperty(
        "--winner-color",
        winner.color
      );

      // Reveal the winner
      winnerPanel.hidden = false;

      openButton.disabled = false;

    }, 6300);
  } catch (error) {
    result.textContent = `Could not open the case: ${error.message}`;
    openButton.disabled = false;
  }
}

buildReel(randomItem());
openButton.addEventListener("click", openCase);
