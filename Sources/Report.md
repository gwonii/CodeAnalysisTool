### Differentiable.swift

| Protocol              | Description                                                                                                   |
|-----------------------|---------------------------------------------------------------------------------------------------------------|
| ContentEquatable      | Represents a value that can compare whether the content are equal.                                           |
| ContentIdentifiable   | Represents the value that identified for differentiate.                                                     |
| DifferentiableSection | Represents the section of collection that can be identified and compared to whether has updated.            |
| Differentiable        | Represents a type that can be used for identifying and comparing for equality.                               |

| Class    | Description                                                                                                                            |
|----------|----------------------------------------------------------------------------------------------------------------------------------------|
| Changeset | A set of changes in the sectioned collection. Changes to the section of the linear collection should be empty.                           |

| Struct    | Description                                                                                                                           |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------|
| HashablePair   | A private struct used in `Changeset` for mapping pairs of source and target offsets or paths.                                       |

