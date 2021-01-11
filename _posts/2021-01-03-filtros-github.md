---
title: 'Fitros Github'
date: 2021-01-03
permalink: /posts/fitros-github
tags:
  - github
---

Eu fico meio perdido em achar Issues e Pull Request no github,
segue-se alguns filtros que costumo usar:

Issues abertas que eu criei:
{% highlight shell %}
is:open is:issue author:thiagogomesverissimo
{% endhighlight %}

Issues abertas que eu participo:
{% highlight shell %}
involves:thiagogomesverissimo is:issue is:open
{% endhighlight %}

Pull requests abertas que eu participo:
{% highlight shell %}
involves:thiagogomesverissimo is:pr is:open
{% endhighlight %}

Pull Requests abertas na organização `fflch`:
{% highlight shell %}
org:fflch is:issue is:open
{% endhighlight %}

Issues abertas na organização `fflch`:
{% highlight shell %}
org:fflch is:issue is:open
{% endhighlight %}



