<?php

// TODO We're missing parentheses for the direct call
assert((fn() => false)());
assert((fn&(int... $args): ?bool => $args[0])(false));

?>