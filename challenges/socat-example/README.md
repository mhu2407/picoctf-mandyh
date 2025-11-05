# Yolosign

The service has two functionality:
* Sign as many messages as the client wants with a RSA key
* Send the flag if the client can forge a signature on a challenge message. The service stops after that, whether the signature was valid or not.

The RSA key is always the same (for an instance). So an attacker can get a challenge, and open a new connection to get it signed.
