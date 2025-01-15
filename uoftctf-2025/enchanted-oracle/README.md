This was an AES challenge.

To root it, we need to exploit a known attack : _AES-CBC padding oracle attack_.

But here, it was a bit tricky cause we _only know the iv and encrypted block of **'random'**_ and have to _give back the corresponding encrypted block of **'I am an authenticated admin, please give me the flag'**_ so as to get the flag.

For that, I dig deeper into _AES-CBC padding oracle attack_ concepts and managed to recover the corresponding enypted blocks of **'I am an authenticated admin, please give me the flag'** using the informations provided by the challenge.

For better explanation, look at _solve folder_. Except **_wu.py_**, the others came from the official [repo](https://github.com/UofTCTF/uoftctf-2025-chals-public/blob/master/enchanted-oracle/solve).

And finally, the flag was : **uoftctf{y3s_1_kn3w_y0u_w3r3_w0r7hy!!!}**.