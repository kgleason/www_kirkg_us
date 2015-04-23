<!--
.. title: Test Markdown Test
.. slug: test-markdown-test
.. date: 2515-04-22 19:07:10 UTC-05:00
.. tags: Test Markdown
.. category:
.. link:
.. description:
.. type: text
-->

# Test Markdown Test


    :::python
    import sys

    def survivor(n):
	    iter = 0
	    r = 0
	    for i in range(1 , n+1):
		    iter = iter + 1
		    print("On iteration {0}".format(iter))
		    print("({0} + 2) % {1}".format(r, i))
		    r = (r + 2)%i
	    return r

    print(survivor(int(sys.argv[1])))


That should be a colored code block
