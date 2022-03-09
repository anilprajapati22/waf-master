#!/bin/bash

echo "<h1 id="id1" >Hostname :  </br> $(hostname)</h1>" > index.html
/usr/sbin/apache2 -D FOREGROUND

