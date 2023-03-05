<?php
function dump_attributes($attributes) {
    $arr = [];
    foreach ($attributes as $attribute) {
        $arr[] = ['name' => $attribute->getName(), 'args' => $attribute->getArguments()];
    }
    var_dump($arr);
}

namespace Doctrine\ORM\Mapping {
    class Entity {
    }
}

namespace Doctrine\ORM\Attributes {
    class Table {
    }
}

namespace Foo {
    use Doctrine\ORM\Mapping\Entity;
    use Doctrine\ORM\Mapping as ORM;
    use Doctrine\ORM\Attributes;

    <<Entity("imported class")>>
    <<ORM\Entity("imported namespace")>>
    <<\Doctrine\ORM\Mapping\Entity("absolute from namespace")>>
    <<\Entity("import absolute from global")>>
    <<Attributes\Table()>>
    function foo() {
    }
}

namespace {
    class Entity {}

    dump_attributes((new ReflectionFunction('Foo\foo'))->getAttributes());
}
?>