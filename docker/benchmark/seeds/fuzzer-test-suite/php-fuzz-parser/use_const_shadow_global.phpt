<?php

namespace {
    require 'includes/global_bar.inc';
    require 'includes/foo_bar.inc';
}

namespace {
    var_dump(bar);
}

namespace {
    use const foo\bar;
    var_dump(bar);
    echo "Done\n";
}

?>