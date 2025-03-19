
    document.addEventListener("DOMContentLoaded", function() {
        function updateSeasonalContent() {
            const now = new Date();
            const year = now.getFullYear();
            const springStart = new Date(year, 2, 1); // March 1
            const summerStart = new Date(year, 5, 1); // June 1
            const autumnStart = new Date(year, 8, 1); // September 1
            const winterStart = new Date(year, 11, 1); // December 1

            let season, seasonInfo, beerChoice;

            if (now >= springStart && now < summerStart) {
                season = "Spring";
                seasonInfo = "Spring heralds a shift in stock to accommodate warmer weather and renewed guest activity. You should be pushing items that are light and in the build up to the summer season. Expect and uprise in lighter ales and floral cocktails, come up with some specials that pair well with crisp wines to match the seasons fresh, vibrant mood. Align your menu's with the season and offer some lighter and fresh meals.";
                beerChoice = "Corona";
                wineChoice = "Prosecco";
                cocktailChoice = "Mojito";


            } else if (now >= summerStart && now < autumnStart) {
                season = "Summer";
                seasonInfo = "Summer brings a peak in guest attendance, prompting a vibrant shift in hospitality stock to suit long, sunny days and balmy nights. It's time to highlight refreshing beverages and summer-centric dishes. Stock up on seasonal beers, fruity cocktails, and chilled rosés perfect for outdoor dining. Specials should include dishes that feature fresh, local produce and light seafood. Design your menus to embody the spirit of relaxation and leisure, appealing to those looking to savor the essence of summer.";
                beerChoice = "Bira Moretti";
                wineChoice = "Pinot Grigio";
                cocktailChoice = "Aperol Spritz";


            } else if (now >= autumnStart && now < winterStart) {
                season = "Fall";
                seasonInfo = "Fall marks a transition to cozier offerings in the hospitality sector as cooler weather sets in. It's the ideal time to introduce heartier fare and warm, spiced drinks that resonate with the season's essence. Stock should include robust ales, rich red wines, and ciders that complement dishes featuring autumnal flavors like pumpkin, squash, and root vegetables. Consider creating specials that invoke a sense of comfort, such as stews and baked goods, to attract guests seeking warmth and comfort in their dining experiences.";
                beerChoice = "Bira Moretti";
                wineChoice = "Rijoca";
                cocktailChoice = "Negroni";


            } else {
                season = "Winter";
                seasonInfo = "Winter in the hospitality industry calls for a warm and inviting atmosphere as guests seek comfort from the cold. Stock up on ingredients for hot, comforting beverages like mulled wine, hot toddies, and rich, dark ales. Emphasize dishes that offer warmth and sustenance, such as hearty soups, stews, and roasted meats. Incorporate seasonal spices like cinnamon and nutmeg to enhance the festive feeling. Creating a cozy environment with these winter favorites can make your establishment a preferred retreat during the chilly season.";
                beerChoice = "N/A";
                wineChoice = "Merlot";
                cocktailChoice = "Hot Toddy";
            }

            document.querySelector("h2").textContent = season;
            document.querySelector(".season-info .season-box p").textContent = seasonInfo;
            document.querySelector(".choices .choice.beer p").textContent = `Beer Choice || ${beerChoice}`;
            document.querySelector(".choices .choice.wine p").textContent = `Wine Choice || ${wineChoice}`;
            document.querySelector(".choices .choice.cocktail p").textContent = `Cocktail Choice || ${cocktailChoice}`;
        }

        updateSeasonalContent(); // Call this function on page load
    });
