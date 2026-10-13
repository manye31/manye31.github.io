---
layout: page
title: Hobbies
permalink: /hobbies/
nav: false
sitemap: false
images:
  slider: true
---
I do lots of things outside research. I am a huge fan of film and music. I love playing video games and board games, and I love hiking. I also love collecting physical media (vinyls, movies, video games, books). Check out some of my favs and my collection below!

<div class="hobbies" data-style="bar" markdown="1">

<details class="hobby" id="music" markdown="1" open style="--hobby-color: #1db954">
<summary><h2>🎧 Music</h2></summary>

I've lived in the past for years. Funk, Soul, and R&B from the 70's are my favorite (EW&F, Redbone, Stevie Wonder, Parliament, Elton John), but I like Rock too (ELO, Hall&Oates). As a saxophone player, I love Jazz too. Recently, I've entered the modern era and have been listening to some Kendrick, Bad Bunny, and Tyler. I also jam to musicals here and there. You can peruse my recent music tastes and see my vinyl collection as well. Updated live!

<div class="music-showcase" data-layout="side-right">
  <div class="ms-spotify">
    <h3>My recent grooves</h3>
    {% include spotify_wrapped.liquid %}
  </div>
  <div class="ms-discogs">
    <h3>My vinyl collection</h3>
    {% include discogs_mosaic.liquid username="manye31" %}
  </div>
</div>

</details>

<details class="hobby" id="film" markdown="1" style="--hobby-color: #ff8000">
<summary><h2>🎥 Film</h2></summary>

During Covid, I watched over 300 movies. Nowadays, I still try to watch quite a few. Some of my favorites: 12 Angry Men, Good Morning Vietnam, Death of Stalin, Inception, Revenge of the Sith, Pulp Fiction, Godfather, too many more. Big fan of Star Wars (like BIG FAN), LoTR, and Dune series.

Movie info and stats coming soon ^^

</details>

<details class="hobby" id="gaming" markdown="1" style="--hobby-color: #7c5cff">
<summary><h2>🎮/🎲 Gaming</h2></summary>

I'm a big fan of video games but don't get to it as often. Some of my favorite franchises are Zelda, Kirby, Mario, Pikmin, Splatoon (yeah big Nintendo guy), Portal, Roller Coaster Tycoon, lots of LEGO games. I have been collecting a physical video game collection with Switch, Wii, PS4, XBox 360 consoles at my apartment and a variety of games for each. I collect Kirby plushies too.

I grew up in an intense board game family. We gamed all the time. I started playing Ticket to Ride when I was 4 years old. Some of my favorites are TTR, SkyTeam, Splendor, Catan. I've gotten quite a collection of games nowadays as well. 

Games info and stats coming soon ^^

</details>

<details class="hobby" id="hiking" markdown="1" style="--hobby-color: #3b8bd9">
<summary><h2>🥾 Hiking</h2></summary>

I like to hike too. Some pics coming soon ^^

</details>

</div>

<script>
  // Open a section when the page is linked with its name, e.g. /hobbies/#music
  (function () {
    function openFromHash() {
      var target = location.hash && document.getElementById(location.hash.slice(1));
      if (target && target.tagName === 'DETAILS') {
        target.open = true;
        target.scrollIntoView();
      }
    }
    openFromHash();
    window.addEventListener('hashchange', openFromHash);
  })();
</script>

{% comment %}
  Photo slider, same as on the summer camp page. Put photos in assets/img/hobbies/, copy this into a section above,
  and move it out of the comment:

<swiper-container slides-per-view="2.2" space-between="16" centered-slides="true" keyboard="true" navigation="true" loop="true" autoplay-delay="3500" autoplay-disable-on-interaction="false">
  <swiper-slide>{% include figure.liquid loading="eager" path="assets/img/hobbies/photo1.jpg" class="img-fluid rounded z-depth-1" %}</swiper-slide>
  <swiper-slide>{% include figure.liquid loading="eager" path="assets/img/hobbies/photo2.jpg" class="img-fluid rounded z-depth-1" %}</swiper-slide>
</swiper-container>
{% endcomment %}
