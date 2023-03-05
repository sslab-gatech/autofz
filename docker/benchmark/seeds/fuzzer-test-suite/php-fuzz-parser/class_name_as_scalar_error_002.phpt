<?php

namespace Foo\Bar {
    class One {
        const Baz = parent::class;
    }
    var_dump(One::Baz);
}
?>