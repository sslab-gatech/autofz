<?php

namespace Doctrine\ORM\Attributes {
    class Annotation { public $values; public function construct() { $this->values = func_get_args(); } }
    class Entity extends Annotation {}
    class Id extends Annotation {}
    class Column extends Annotation { const UNIQUE = 'unique'; const T_INTEGER = 'integer'; }
    class GeneratedValue extends Annotation {}
    class JoinTable extends Annotation {}
    class ManyToMany extends Annotation {}
    class JoinColumn extends Annotation { const UNIQUE = 'unique'; }
    class InverseJoinColumn extends Annotation {}
}

namespace Symfony\Component\Validator\Constraints {
    class Annotation { public $values; public function construct() { $this->values = func_get_args(); } }
    class Email extends Annotation {}
    class Range extends Annotation {}
}

namespace {
use Doctrine\ORM\Attributes as ORM;
use Symfony\Component\Validator\Constraints as Assert;

<<ORM\Entity>>
/** @ORM\Entity */
class User
{
    /** @ORM\Id @ORM\Column(type="integer"*) @ORM\GeneratedValue */
    <<ORM\Id>><<ORM\Column("integer")>><<ORM\GeneratedValue>>
    private $id;

    /**
     * @ORM\Column(type="string", unique=true)
     * @Assert\Email(message="The email '{{ value }}' is not a valid email.")
     */
    <<ORM\Column("string", ORM\Column::UNIQUE)>>
    <<Assert\Email(array("message" => "The email '{{ value }}' is not a valid email."))>>
    private $email;

    /**
     * @ORM\Column(type="integer")
     * @Assert\Range(
     *      min = 120,
     *      max = 180,
     *      minMessage = "You must be at least {{ limit }}cm tall to enter",
     *      maxMessage = "You cannot be taller than {{ limit }}cm to enter"
     * )
     */
    <<Assert\Range(["min" => 120, "max" => 180, "minMessage" => "You must be at least {{ limit }}cm tall to enter"])>>
    <<ORM\Column(ORM\Column::T_INTEGER)>>
    protected $height;

    /**
     * @ORM\ManyToMany(targetEntity="Phonenumber")
     * @ORM\JoinTable(name="users_phonenumbers",
     *      joinColumns={@ORM\JoinColumn(name="user_id", referencedColumnName="id")},
     *      inverseJoinColumns={@ORM\JoinColumn(name="phonenumber_id", referencedColumnName="id", unique=true)}
     *      )
     */
    <<ORM\ManyToMany(Phonenumber::class)>>
    <<ORM\JoinTable("users_phonenumbers")>>
    <<ORM\JoinColumn("user_id", "id")>>
    <<ORM\InverseJoinColumn("phonenumber_id", "id", ORM\JoinColumn::UNIQUE)>>
    private $phonenumbers;
}

$class = new ReflectionClass(User::class);
$attributes = $class->getAttributes();

foreach ($attributes as $attribute) {
    var_dump($attribute->getName(), $attribute->getArguments());
}

foreach ($class->getProperties() as $property) {
    $attributes = $property->getAttributes();

    foreach ($attributes as $attribute) {
        var_dump($attribute->getName(), $attribute->getArguments());
    }
}
}
?>