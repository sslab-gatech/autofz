<?php

1 ? 2 : 3 ? 4 : 5;   // deprecated
(1 ? 2 : 3) ? 4 : 5; // ok
1 ? 2 : (3 ? 4 : 5); // ok

// While the associativity of ?: is also incorrect, it will not cause a
// functional difference, only some unnecessary checks.
1 ?: 2 ?: 3;   // ok
(1 ?: 2) ?: 3; // ok
1 ?: (2 ?: 3); // ok

1 ?: 2 ? 3 : 4;   // deprecated
(1 ?: 2) ? 3 : 4; // ok
1 ?: (2 ? 3 : 4); // ok

1 ? 2 : 3 ?: 4;   // deprecated
(1 ? 2 : 3) ?: 4; // ok
1 ? 2 : (3 ?: 4); // ok

?>