
function clickedLinkVertigo(link,event,title) {

    event.preventDefault();

    var buttons = document.getElementsByClassName('vertigopage__sibling');

    for (var i = 0; i < buttons.length; i++)
    {
        var buttonLink = buttons[i];

        buttonLink.style.display = 'none';
        buttonLink.classList.remove('active');

        if (buttonLink.text === title)
        {
            buttonLink.style.display = 'block';
            buttonLink.classList.add('active');
        }
    }
}
