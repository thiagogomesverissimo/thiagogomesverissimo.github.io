---
title: 'Github search filters'
date: 2021-01-03
permalink: /posts/github-search-filters
tags:
  - github
redirect_from:
  - /posts/fitros-github
---

When navigating GitHub, it is often advantageous to establish custom filters for efficiently locating issues or pull requests associated with either yourself, a friend or a company.I have prepared a list of useful way to create some filters. <br><br>

List open issues that belongs to me:
{% highlight shell %}
is:open is:issue author:thiagogomesverissimo
{% endhighlight %}

List open issues I am involved:
{% highlight shell %}
involves:thiagogomesverissimo is:issue is:open
{% endhighlight %}

List open pull requests I am involved:
{% highlight shell %}
involves:thiagogomesverissimo is:pr is:open
{% endhighlight %}

List open pull requests from a organization named `fflch`:
{% highlight shell %}
org:fflch is:pr is:open
{% endhighlight %}

List open issues from a organization named `fflch`:
{% highlight shell %}
org:fflch is:issue is:open
{% endhighlight %}



