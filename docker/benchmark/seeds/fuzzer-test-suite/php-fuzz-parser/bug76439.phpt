<?php

[$one, $two, $three, $four, $five, $six, $seven, $eight, $nine] = [1, 2, 3, 4, 5, 6, 7, 8, 9];

var_dump(<<<BAR
 $one-
 BAR);

var_dump(<<<BAR
 $two -
 BAR);

var_dump(<<<BAR
 $three	-
 BAR);

var_dump(<<<BAR
 $four-$four
 BAR);

var_dump(<<<BAR
 $five-$five-
 BAR);

var_dump(<<<BAR
 $six-$six-$six
 BAR);

var_dump(<<<BAR
 $seven
 -
 BAR);

var_dump(<<<BAR
 $eight
  -
 BAR);

var_dump(<<<BAR
$nine
BAR);

var_dump(<<<BAR
 -
 BAR);

var_dump(<<<BAR
  -
 BAR);

?>