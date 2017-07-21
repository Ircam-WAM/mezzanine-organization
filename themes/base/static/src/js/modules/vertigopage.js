function clickedLinkVertigo(link,event) {

    event.preventDefault();

    var buttons = document.getElementsByClassName('vertigopage__button');

    for (var i = 0; i < buttons.length; i++)
    {
        var indexItem = i + 1;
        var buttonLink = buttons[i];

        buttonLink.classList.remove('vertigopage__selected');
        buttonLink.classList.remove('vertigopage__unselected');

        var contentText = document.getElementById("content-" + indexItem);

        contentText.classList.remove('vertigopage__visible');
        contentText.classList.remove('vertigopage__invisible');

        if (link.id === "link-" + indexItem)
        {
            buttonLink.classList.add('vertigopage__selected');
            contentText.classList.add('vertigopage__visible');
        }
        else
        {
            buttonLink.classList.add('vertigopage__unselected');
            contentText.classList.add('vertigopage__invisible');
        }
    }
}