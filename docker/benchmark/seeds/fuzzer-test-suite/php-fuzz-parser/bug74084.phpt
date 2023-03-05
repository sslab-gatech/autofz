<?php
$$A += $$B['a'] = &$$C;
unset($$A);
try {
    $$A -= $$B['a'] = &$$C;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
unset($$A);
try {
    $$A *= $$B['a'] = &$$C;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
unset($$A);
try {
    $$A /= $$B['a'] = &$$C;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
unset($$A);
try {
    $$A **= $$B['a'] = &$$C;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
?>