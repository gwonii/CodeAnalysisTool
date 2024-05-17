### SupplementaryView.swift

| Property      | Type          | Description                               |
|---------------|---------------|-------------------------------------------|
| component     | AnyComponent  | A type-erased component for supplementary view. |
| kind          | String        | The kind of the supplementary view.       |
| alignment     | NSRectAlignment | The alignment of the supplementary view. |
| eventStorage  | ListingViewEventStorage | A storage for event handling in `SupplementaryView`. |

| Method                         | Parameters                             | Return Type   | Description                 |
|--------------------------------|----------------------------------------|---------------|-----------------------------|
| init                           | kind: String, component: some Component, alignment: NSRectAlignment | None  | Initializes the `SupplementaryView` with the given parameters. |
| willDisplay                    | handler: (WillDisplayEvent.EventContext) -> Void | SupplementaryView | Registers a callback handler for when the component is displayed on the screen. |
| didEndDisplaying               | handler: (DidEndDisplayingEvent.EventContext) -> Void | SupplementaryView | Registers a callback handler for when the component is removed from the screen. |

The `SupplementaryView` struct represents a supplementary view in a `UICollectionView`. It contains properties for the type-erased component, kind, alignment, and event storage. The `init` method initializes a `SupplementaryView` with the specified kind, component, and alignment.

The `willDisplay` method allows registering a callback handler that is triggered when the component is displayed on the screen, while the `didEndDisplaying` method registers a callback handler for when the component is removed from the screen.

Overall, `SupplementaryView` provides a way to encapsulate supplementary view-related information and event handling logic for use within a UICollectionView.

### Cell.swift

| Property       | Type          | Description                                  |
|----------------|---------------|----------------------------------------------|
| id             | AnyHashable   | Identifier that identifies the Cell          |
| component      | AnyComponent  | Type-erased component for the cell           |
| eventStorage   | ListingViewEventStorage | Storage for listing view events        |

| Method                       | Parameter                           | Return Type           | Description                                                                     |
|------------------------------|-------------------------------------|-----------------------|---------------------------------------------------------------------------------|
| init(id:component:)          | id: some Hashable, component: some Component | Void              | Initializes a Cell with the given id and component                               |
| init(component:)              | component: some IdentifiableComponent | Void              | Initializes a Cell with the given IdentifiableComponent                          |
| didSelect(_)                 | handler: (DidSelectEvent.EventContext) -> Void | Cell        | Registers a callback handler for the select event                                |
| willDisplay(_)               | handler: (WillDisplayEvent.EventContext) -> Void | Cell      | Registers a callback handler for the will display event                           |
| didEndDisplay(_)             | handler: (DidEndDisplayingEvent.EventContext) -> Void | Cell | Registers a callback handler for the did end display event              |

### 핵심로직
- `Cell` 구조체는 `Identifiable`을 채택하고, `ListinViewEventHandler` 프로토콜을 준수합니다.
- 각 셀은 id와 컴포넌트를 가지고 있으며, 해당 셀에 대한 이벤트 핸들러를 등록할 수 있습니다.
- `Hashable`을 구현하여 셀의 동등성 비교가 가능합니다.
- `Differentiable`을 채택하고 `differenceIdentifier` 및 `isContentEqual` 메서드를 구현하여 셀 간의 차이를 파악합니다.

### List.swift

| Property Name | Type               | Description                            |
|---------------|--------------------|----------------------------------------|
| sections      | [Section]          | An array of sections to be displayed on the screen. |


| Method Name           | Parameters                        | Return Type             | Description                                                           |
|-----------------------|-----------------------------------|-------------------------|-----------------------------------------------------------------------|
| init(sections:)       | sections: [Section]               | Void                    | Initializes a List with the provided sections array.                 |
| init(@SectionsBuilder) | sections: () -> [Section]         | Void                    | Initializes a List with a builder closure that creates sections.     |
| didScroll             | handler: (DidScrollEvent.EventContext) -> Void | Void  | Registers a callback handler for when the user scrolls the content view. |
| onRefresh             | handler: (PullToRefreshEvent.EventContext) -> Void | Void | Registers a callback handler for when the user pulls to refresh.     |
| willBeginDragging     | handler: (WillBeginDraggingEvent.EventContext) -> Void | Void | Registers a callback handler for when the scrollView begins scrolling. |
| willEndDragging       | handler: (WillEndDraggingEvent.EventContext) -> Void | Void | Registers a callback handler for when the user finishes scrolling the content.   |


The `List` struct represents a collection view with multiple sections. It contains an array of sections, and provides methods to handle scroll events and pull-to-refresh functionality. Sections can be initialized either by providing an array directly or by using a builder closure.

The key logic involves registering event handlers for various scroll-related actions such as scrolling, pull-to-refresh, and dragging events. These event handlers allow the `List` to respond to user interactions and update the UI accordingly.

### Section.swift

| Property             | Type                       | Description                                     |
|----------------------|----------------------------|-------------------------------------------------|
| id                   | AnyHashable                | Identifier for the Section                      |
| header               | SupplementaryView?         | Represents the header view of the Section      |
| cells                | [Cell]                     | Array of cells representing UICollectionViewCells |
| footer               | SupplementaryView?         | Represents the footer view of the Section      |
| nextBatchTrigger     | NextBatchTrigger?          | Encapsulates information about next batch updates |
| sectionLayout        | CompositionalLayoutSectionFactory.SectionLayout? | Custom section layout provider |

| Method                        | Parameters                                  | Return Type | Description                                    |
|------------------------------|---------------------------------------|------------|-----------------------------------------------|
| init(id:cells:)                          | id: Hashable, cells: [Cell]                | Section    | Initializes the Section with an identifier and array of cells |
| withSectionLayout(_:layoutMaker:)        | sectionLayout: CompositionalLayoutSectionFactory.SectionLayout?           | Section | Sets the custom layout for the Section |
| withHeader(_:alignment:)                  | headerComponent: Component, alignment: NSRectAlignment | Section  | Sets the header for the Section with alignment |
| withFooter(_:alignment:)                  | footerComponent: Component, alignment: NSRectAlignment       | Section  | Sets the footer for the Section with alignment |
| withNextBatchTrigger(_:trigger:)            | trigger: NextBatchTrigger?                         | Section  | Sets the next batch trigger for the Section |

The `Section` struct represents a section in a UICollectionView. It contains properties like id, header, cells, footer, nextBatchTrigger, and sectionLayout. The key logic lies in setting the layout for the section and handling events related to the header and footer.

- The `withSectionLayout` method allows users to specify custom layout for the section using different factory objects.
- The `withHeader` and `withFooter` methods set the header and footer components for the section, including alignment options.
- The `withNextBatchTrigger` method enables pagination support by setting the trigger for the timing of the next batch update.

Overall, the `Section` struct encapsulates the necessary information and logic to define a section in a UICollectionView with various customization options for layout and UI elements.

### Extension/UICollectionView+Difference.swift

| Property                  | Type                              | Description                             |
|---------------------------|-----------------------------------|-----------------------------------------|
| stagedChangeset           | StagedChangeset<C>                | StagedChangeset를 저장하는 프로퍼티         |
| interrupt                 | ((Changeset<C>) -> Bool)?         | 변경을 중단할지 여부를 확인하는 클로저를 저장하는 프로퍼티 |
| setData                   | (C) -> Void                       | 데이터를 설정하는 클로저를 저장하는 프로퍼티   |
| completion                | ((Bool) -> ())?                   | 업데이트가 완료됐을 때 호출될 클로저를 저장하는 프로퍼티 |

| Method                                      | Parameter                              | Return Type | Description |
|---------------------------------------------|----------------------------------------|-------------|-------------|
| reload(using:interrupt:setData:completion:) | stagedChangeset: StagedChangeset<C>, interrupt: ((Changeset<C>) -> Bool)?, setData: (C) -> Void, completion: ((Bool) -> ())? | Void | UICollectionView를 업데이트하기 위한 메서드로, StagedChangeset에 따라 UI를 업데이트하고 completion 클로저를 호출한다. 중간에 변경을 중단할 수 있는 interrupt 클로저를 제공할 수 있으며, 마지막 클로저가 실행된 후 completion 클로저를 호출한다. |

이 코드는 UICollectionView의 확장(extension)으로, `reload` 메서드를 제공한다. 이 메서드는 StagedChangeset를 사용하여 UICollectionView를 업데이트하고, 각 업데이트 단계마다 completion 클로저를 호출한다. 변경을 중단할 경우에 interrupt 클로저를 사용할 수 있으며, 모든 업데이트가 완료된 후에 completion 클로저를 호출한다. 업데이트 과정에서 section 및 element의 삽입, 삭제, 업데이트, 이동에 대한 로직이 구현되어 있어, UICollectionView가 변경 사항을 반영하는데 사용될 수 있다.

### Extension/UICollectionView+Init.swift

| Property         | Type                                                 | Description                                          |
|------------------|------------------------------------------------------|------------------------------------------------------|
| layoutAdapter    | CollectionViewLayoutAdaptable                        | A property to hold an instance of `CollectionViewLayoutAdaptable`, which is used to configure the collection view layout. |

| Method                                | Parameters                           | Return Type                | Description                                                                                                                                                   |
|---------------------------------------|--------------------------------------|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| init(layoutAdapter:)                  | layoutAdapter: CollectionViewLayoutAdaptable | UICollectionView            | A convenience initializer for `UICollectionView` that takes a `CollectionViewLayoutAdaptable` and configures the collection view with a compositional layout.   |

**Core logic:**
- `UICollectionView`의 convenience 초기화 메서드는 `CollectionViewLayoutAdaptable` 프로토콜을 구현한 객체를 인자로 받아와서 컬렉션 뷰의 레이아웃을 구성한다.
- `UICollectionViewCompositionalLayout`를 사용하여 섹션 레이아웃을 제공하는 구성 요소를 생성하여 컬렉션 뷰의 레이아웃을 설정한다.

### Prefetching/RemoteImagePrefetching.swift

| Property         | Type                   | Description                 |
|------------------|-------------------------|-----------------------------|
| `remoteImageManager` | `RemoteImagePrefetching` | An object conforming to the `RemoteImagePrefetching` protocol for managing remote image prefetching tasks. |

| Method             | Parameter           | Return Type     | Description                                                            |
|---------------------|---------------------|-----------------|------------------------------------------------------------------------|
| `prefetchImage(url:)` | `url: URL`            | `UUID?`         | Prefetches an image from the given URL and returns a UUID for the task. |
| `cancelTask(uuid:)`   | `uuid: UUID`          | `Void`          | Cancels a prefetch task using the given UUID.                          |

**핵심 로직:**
이 코드는 원격 이미지를 미리 가져오는 동작을 담당하는 `RemoteImagePrefetching` 프로토콜을 정의하고 있습니다. `RemoteImageManager` 클래스는 이 프로토콜을 구현한 객체로, 원격 이미지의 미리 가져오기 작업을 관리합니다. `prefetchImage(url:)` 메서드를 사용하여 주어진 URL에서 이미지를 미리 가져 오는 작업을 시작하고 해당 작업에 대한 UUID를 반환합니다. 이후에 이 UUID를 사용하여 `cancelTask(uuid:)` 메소드를 사용해 원격 이미지의 미리 가져오기 작업을 취소할 수 있습니다.

### Prefetching/PrefetchableComponent.swift

| 구조체 이름: ComponentRemoteImagePrefetchable |
|-------------------|-------------------------------------|
| Property          | Type                               |
|-------------------|-------------------------------------|
| remoteImageURLs   | [URL]                             |
|-------------------|-------------------------------------|

- Property:
  - remoteImageURLs: 미리 가져와야 하는 원격 이미지의 URL 목록을 저장하는 배열

- Method:
  - prefetchRemoteImages(completionHandler:): 원격 이미지를 미리 가져오는 함수
    - Parameters: completionHandler - 이미지 미리 가져오기 작업 완료 시 실행할 클로저
    - Return Type: Void

- 핵심 로직:
  - prefetchRemoteImages(completionHandler:) 메서드를 호출하면 해당 구조체가 갖고 있는 remoteImageURLs 배열에 있는 모든 원격 이미지 URL을 가져와서 메모리에 캐시하는 역할을 수행함.
  - completionHandler 클로저는 이미지 미리 가져오기 작업이 완료된 후 실행되어 추가적인 작업(예: UI 업데이트)을 수행할 수 있도록 함.

### Prefetching/Plugins/CollectionViewPrefetchingPlugin.swift

| Property          | Type                           | Description                                                  |
|-------------------|--------------------------------|--------------------------------------------------------------|
| prefetchHandler   | ((ComponentResourcePrefetchable) -> AnyCancellable?)? | Component 리소스를 prefetch 하는 작업을 수행하는 클로저     |

| Method                               | Parameter                                | Return Type                                | Description                                                       |
|--------------------------------------|------------------------------------------|--------------------------------------------|-------------------------------------------------------------------|
| prefetch(with:)                      | component: **ComponentResourcePrefetchable** | **AnyCancellable?**                        | 주어진 component가 필요로 하는 리소스를 prefetch 하는 작업을 수행하는 함수. prefetch 작업을 취소하기 위한 인스턴스를 반환함. |

**핵심 로직:**  
`prefetch(with:)` 메서드는 주어진 `component`에 필요한 리소스를 prefetch하는 작업을 수행합니다. 이를 위해 인자로 전달된 `ComponentResourcePrefetchable` 프로토콜을 준수하는 객체에 필요한 리소스 prefetch 클로저를 실행하고, prefetch 작업을 취소할 수 있는 인스턴스를 반환합니다. 이를 통해 CollectionViewPrefetchingPlugin 프로토콜을 준수하는 객체는 prefetching을 효율적으로 수행할 수 있습니다.

### Prefetching/Plugins/RemoteImagePrefetchingPlugin.swift

| Property                   | Type                          | Description                                            |
|---------------------------|-------------------------------|--------------------------------------------------------|
| remoteImagePrefetcher     | RemoteImagePrefetching        | An instance of a type conforming to RemoteImagePrefetching protocol used to prefetch remote images. |

| Method                               | Parameters                                        | Return Type                                      | Description                                                                                                                     |
|--------------------------------------|---------------------------------------------------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| init(remoteImagePrefetcher:)    | remoteImagePrefetcher: RemoteImagePrefetching          | N/A                                        | Initializes a new instance of RemoteImagePrefetchingPlugin with a remoteImagePrefetcher instance passed as a parameter.    |

### 핵심 로직:
1. `prefetch(with:)` 메서드를 사용하여 주어진 component의 리소스를 미리 가져옵니다.
2. 입력된 component가 ComponentRemoteImagePrefetchable 형식이 아닌 경우, prefetch 작업을 수행하지 않습니다.
3. ComponentRemoteImagePrefetchable에 정의된 remoteImageURLs를 사용하여 prefetchImage 메서드를 호출하고, 반환된 UUID들을 수집합니다.
4. prefetchImage 메서드는 RemoteImagePrefetching 프로토콜을 준수하는 인스턴스를 사용하여 원격 이미지를 미리 가져오는 작업을 수행하고, 해당 작업의 UUID 값을 반환합니다.
5. 반환된 UUID들을 사용하여 이후 작업에서 이들을 취소할 수 있도록 AnyCancellable 인스턴스를 반환합니다.
6. cancelTask 메서드를 사용하여 필요한 경우 이미지 prefetch 작업을 취소시킬 수 있습니다.

### Layout/DefaultCompositionalLayoutSectionFactory.swift

| Property                       | Type                                                       | Description                                                               |
|--------------------------------|------------------------------------------------------------|---------------------------------------------------------------------------|
| spec                           | DefaultCompositionalLayoutSectionFactory.LayoutSpec?       | Define the type of layout specification for the section factory          |
| sectionContentInsets           | NSDirectionalEdgeInsets?                                    | Insets for the section                                                     |
| headerPinToVisibleBounds       | Bool?                                                      | Indicates whether the header should pin to the top of the visible bounds  |
| footerPinToVisibleBounds       | Bool?                                                      | Indicates whether the footer should pin to the bottom of the visible bounds|
| visibleItemsInvalidationHandler| NSCollectionLayoutSectionVisibleItemsInvalidationHandler? | Handler for invalidating visible items in the section                      |

| Method                                                        | Parameters                                                                    | Return Type                         | Description                                                                    |
|---------------------------------------------------------------|-------------------------------------------------------------------------------|-------------------------------------|--------------------------------------------------------------------------------|
| makeSectionLayout()                                           | None                                                                          | SectionLayout?                      | Creates a section layout based on the specified layout spec                     |
| withSectionContentInsets(_ insets: NSDirectionalEdgeInsets)    | insets: NSDirectionalEdgeInsets                                               | DefaultCompositionalLayoutSectionFactory | Sets the insets for the section                                               |
| withHeaderPinToVisibleBounds(_ pinToVisibleBounds: Bool)      | pinToVisibleBounds: Bool                                                      | DefaultCompositionalLayoutSectionFactory | Sets whether the header should pin to visible bounds                           |
| withFooterPinToVisibleBounds(_ pinToVisibleBounds: Bool)      | pinToVisibleBounds: Bool                                                      | DefaultCompositionalLayoutSectionFactory | Sets whether the footer should pin to visible bounds                           |
| withVisibleItemsInvalidationHandler(_ handler: NSCollectionLayoutSectionVisibleItemsInvalidationHandler) | handler: NSCollectionLayoutSectionVisibleItemsInvalidationHandler | DefaultCompositionalLayoutSectionFactory | Sets the handler for invalidating visible items                                 |

The core logic of the `DefaultCompositionalLayoutSectionFactory` is to provide a default factory that generates different types of compositional layout sections based on the specified layout specifications. It allows users to easily create vertical, horizontal, or grid layouts with customizable settings such as spacing, scrolling behavior, number of items in a row, and insets.

Users can use this factory to quickly set up complex UI layouts with minimal code by selecting the desired layout spec and customizing additional options like section insets, header and footer pinning behavior, and visible items invalidation handling. The `makeSectionLayout()` method is responsible for creating the actual `SectionLayout` based on the selected layout spec and additional settings provided by the user.

### Layout/VerticalGridLayout.swift

| Property                | Type                                             | Description                                                      |
|-------------------------|--------------------------------------------------|------------------------------------------------------------------|
| numberOfItemsInRow      | Int                                              | 한 행에 표시할 아이템의 개수를 설정하는 프로퍼티                |
| itemSpacing            | CGFloat                                          | 아이템 사이의 간격을 설정하는 프로퍼티                           |
| lineSpacing            | CGFloat                                          | 행 사이의 간격을 설정하는 프로퍼티                              |
| sectionInsets          | NSDirectionalEdgeInsets?                         | 섹션의 여백을 설정하는 프로퍼티                                 |
| headerPinToVisibleBounds | Bool?                                            | 헤더를 화면 상단에 고정할지 여부를 설정하는 프로퍼티           |
| footerPinToVisibleBounds | Bool?                                            | 푸터를 화면 하단에 고정할지 여부를 설정하는 프로퍼티           |
| visibleItemsInvalidationHandler | NSCollectionLayoutSectionVisibleItemsInvalidationHandler? | 화면에 보이는 아이템을 업데이트할 때 호출되는 핸들러   |

| Method                                     | Parameter                                         | Return Type           | Description                                                                 |
|--------------------------------------------|---------------------------------------------------|-----------------------|-----------------------------------------------------------------------------|
| init(numberOfItemsInRow:itemSpacing:lineSpacing:) | numberOfItemsInRow: Int, itemSpacing: CGFloat, lineSpacing: CGFloat | Void              | 초기화 메서드로, 한 행에 표시할 아이템의 개수와 간격을 설정한다.              |
| makeSectionLayout()                       | -                                                 | SectionLayout?        | 섹션의 레이아웃을 생성하는 메서드로, NSCollectionLayoutSection을 반환한다.  |
| insets(_: )                               | insets: NSDirectionalEdgeInsets?                  | Self                  | 섹션의 여백을 설정하는 메서드이며, 수정된 인스턴스를 반환한다.               |
| headerPinToVisibleBounds(_: )              | pinToVisibleBounds: Bool?                         | Self                  | 헤더를 화면 상단에 고정할지 여부를 설정하는 메서드로, 수정된 인스턴스를 반환한다. |
| footerPinToVisibleBounds(_: )              | pinToVisibleBounds: Bool?                         | Self                  | 푸터를 화면 하단에 고정할지 여부를 설정하는 메서드로, 수정된 인스턴스를 반환한다. |
| withVisibleItemsInvalidationHandler(_: )   | handler: NSCollectionLayoutSectionVisibleItemsInvalidationHandler? | Self | 화면에 보이는 아이템을 업데이트할 때 호출되는 핸들러를 설정하는 메서드로, 수정된 인스턴스를 반환한다. |

이 코드는 Grid-style vertical scrolling을 지원하는 레이아웃을 정의하기 위한 구조체이다. 주요 기능은 다음과 같다.
1. 한 행에 표시할 아이템의 개수, 간격 등을 설정할 수 있음.
2. 각각의 아이템들을 수평 방향으로 그룹화하고, 이를 다시 수직 방향으로 그룹화하여 섹션의 레이아웃을 생성한다.
3. 섹션의 여백, 헤더 및 푸터의 화면 상단 또는 하단 고정 여부, 화면에 보이는 아이템 업데이트 핸들러 등을 설정할 수 있다.
4. 이러한 설정을 토대로 UICollectionViewCompositionalLayout을 만들어 Grid-style의 화면을 구성한다.

### Layout/HorizontalLayout.swift

| Property                | Type                                      | Description                                           |
|-------------------------|-------------------------------------------|-------------------------------------------------------|
| spacing                 | CGFloat                                   | The spacing between items in the layout. Default value is 0.0. |
| scrollingBehavior       | UICollectionLayoutSectionOrthogonalScrollingBehavior | The behavior of the layout when scrolling. Default value is .continuous. |
| sectionInsets           | NSDirectionalEdgeInsets?                  | The insets for the section.                           |
| headerPinToVisibleBounds| Bool?                                     | Indicates whether the header should pin to visible bounds. |
| footerPinToVisibleBounds| Bool?                                     | Indicates whether the footer should pin to visible bounds. |
| visibleItemsInvalidationHandler | NSCollectionLayoutSectionVisibleItemsInvalidationHandler? | The handler for invalidating visible items.        |

| Method                                               | Parameters                             | Return Type           | Description                                                                                  |
|------------------------------------------------------|----------------------------------------|-----------------------|----------------------------------------------------------------------------------------------|
| init(spacing:scrollingBehavior:)                     | spacing: CGFloat, scrollingBehavior: UICollectionLayoutSectionOrthogonalScrollingBehavior | - | Initializes a new horizontal layout with the given spacing and scrolling behavior.         |
| makeSectionLayout()                                  | -                                      | SectionLayout?        | Creates a layout for a section based on the cell items, section insets, and scrolling behavior. |
| insets(_ insets:)                                   | insets: NSDirectionalEdgeInsets?       | HorizontalLayout       | Sets the insets for the section.                                                             |
| headerPinToVisibleBounds(_ pinToVisibleBounds:)      | pinToVisibleBounds: Bool?              | HorizontalLayout       | Sets whether the header should pin to visible bounds.                                       |
| footerPinToVisibleBounds(_ pinToVisibleBounds:)      | pinToVisibleBounds: Bool?              | HorizontalLayout       | Sets whether the footer should pin to visible bounds.                                       |
| withVisibleItemsInvalidationHandler(_ handler:)      | handler: NSCollectionLayoutSectionVisibleItemsInvalidationHandler? | HorizontalLayout | Sets the handler for invalidating visible items.                                           | 

The HorizontalLayout struct defines a layout for a horizontal scrolling style UI. It allows customization of spacing between items, scrolling behavior, section insets, pinning behavior for header and footer, and a handler for invalidating visible items.

The `makeSectionLayout()` method creates a collection layout section with a horizontal group containing the specified cell items, spacing, insets, and pinning settings. It also configures the orthogonal scrolling behavior and boundary supplementary items (header and footer). Additional customization can be done using the provided setter methods for insets, pinning behavior, and visible items invalidation handler.

### Layout/VerticalLayout.swift

| Property                | Type                                      | Description                                       |
|-------------------------|-------------------------------------------|---------------------------------------------------|
| spacing                 | CGFloat                                   | The spacing between items in the layout.          |
| sectionInsets           | NSDirectionalEdgeInsets?                  | Insets for the section.                           |
| headerPinToVisibleBounds| Bool?                                     | Indicates whether the header should pin to visible bounds. |
| footerPinToVisibleBounds| Bool?                                     | Indicates whether the footer should pin to visible bounds. |
| visibleItemsInvalidationHandler | NSCollectionLayoutSectionVisibleItemsInvalidationHandler? | Handler for invalidating visible items. |

| Method                                      | Parameter              | Return Type             | Description                                         |
|---------------------------------------------|-----------------------|------------------------|-----------------------------------------------------|
| init(spacing:)                              | spacing: CGFloat      | N/A                    | Initializes a new vertical layout with a given spacing. |
| makeSectionLayout()                         | N/A                   | SectionLayout?         | Creates a layout for a section based on the given context. |
| insets(_: )                                 | insets: NSDirectionalEdgeInsets? | Self         | Sets the insets for the section.                    |
| headerPinToVisibleBounds(_: )               | pinToVisibleBounds: Bool? | Self          | Sets whether the header should pin to visible bounds.|
| footerPinToVisibleBounds(_: )               | pinToVisibleBounds: Bool? | Self          | Sets whether the footer should pin to visible bounds.|
| withVisibleItemsInvalidationHandler(_: )    | handler: NSCollectionLayoutSectionVisibleItemsInvalidationHandler? | Self | Sets the handler for invalidating visible items.   |

The `VerticalLayout` struct defines a layout that supports vertical scrolling in a collection view. It allows customization of spacing, section insets, pinning behavior of header and footer, and visible items invalidation handler. The `makeSectionLayout()` method dynamically creates the layout based on the context provided, with options for customizing various layout properties.

### Layout/CompositionalLayoutSectionFactory.swift

| Property            | Type                                     | Description                                  |
|----------------------|------------------------------------------|----------------------------------------------|
| makeSectionLayout    | SectionLayout?                           | Creates a layout closure for a section.     |
|                      |                                          |                                              |
| layoutCellItems      | cells: [Cell],                           | Makes layout items for cells based on size  |
|                      | sizeStorage: ComponentSizeStorage         | storage.                                     |
|                      |                                          |                                              |
| layoutHeaderItem     | section: Section,                        | Makes layout item for a section header.     |
|                      | sizeStorage: ComponentSizeStorage         |                                              |
|                      |                                          |                                              |
| layoutFooterItem     | section: Section,                        | Makes layout item for a section footer.     |
|                      | sizeStorage: ComponentSizeStorage         |                                              |

| Method                             | Parameters                                     | Return Type                          | Description                                                                                         |
|------------------------------------|-------------------------------------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------|
| makeSectionLayout                  | - context: LayoutContext                        | NSCollectionLayoutSection?          | Creates and returns a layout for a section based on the given context.                                |
|                                    |                                                 |                                      |                                                                                                     |
| layoutCellItems                    | - cells: [Cell],                                | [NSCollectionLayoutItem]            | Creates layout items for cells based on their size and layout mode.                                |
|                                    | - sizeStorage: ComponentSizeStorage              |                                      |                                                                                                     |
|                                    |                                                 |                                      |                                                                                                     |
| layoutHeaderItem                   | - section: Section,                             | NSCollectionLayoutBoundarySupplementaryItem? | Creates a layout item for the section header based on its size and alignment.                     |
|                                    | - sizeStorage: ComponentSizeStorage              |                                      |                                                                                                     |
|                                    |                                                 |                                      |                                                                                                     |
| layoutFooterItem                   | - section: Section,                             | NSCollectionLayoutBoundarySupplementaryItem? | Creates a layout item for the section footer based on its size and alignment.                     |
|                                    | - sizeStorage: ComponentSizeStorage              |                                      |                                                                                                     |

The core logic of this protocol involves creating and managing the layout for a section in a collection view. The `makeSectionLayout` method creates and returns a closure that defines the layout for the section. The `layoutCellItems`, `layoutHeaderItem`, and `layoutFooterItem` methods are responsible for creating layout items for cells, section headers, and section footers respectively. These layout items are defined based on the provided cells, sections, and their corresponding sizes from the `ComponentSizeStorage`.

### SwiftUISupport/ComponentRepresented.swift

| Property      | Type               | Description                                   |
|-------------- |--------------------|-----------------------------------------------|
| component     | Generic Type `C`   | Represents the component to be rendered       |

| Method                     | Parameters                 | Return Type   | Description                          |
|----------------------------|----------------------------|---------------|--------------------------------------|
| makeUIView                 | Context                    | `C.Content`   | Creates and returns the rendered content view of the component |
| updateUIView               | `C.Content`, Context        | Void          | Updates the rendered view with the latest data |
| makeCoordinator            | -                          | `C.Coordinator`| Creates and returns the coordinator for the component |

The `ComponentRepresented` struct is a SwiftUI wrapper that allows a custom component (`C`) to be used within a SwiftUI view. It conforms to `UIViewRepresentable` protocol and utilizes three methods - `makeUIView`, `updateUIView`, and `makeCoordinator` - to handle rendering and update operations in SwiftUI.

- The `makeUIView` method creates and returns the rendered content view of the component using the coordinator.
- The `updateUIView` method updates the rendered view with the latest data by passing the existing content view and context.
- The `makeCoordinator` method is responsible for creating and returning the coordinator associated with the component.

By using this struct and the `toSwiftUI` method extension on the `Component` protocol, custom components can be easily integrated into SwiftUI views, enabling seamless migration to SwiftUI from UIKit-based projects.

### Component/IdentifiableComponent.swift

| Property      | Type              | Description                                  |
|--------------|-------------------|----------------------------------------------|
| id           | String            | Unique identifier of the component           |


| Method         | Parameters              | Return Type     | Description                          |
|--------------|-------------------------|-----------------|--------------------------------------|
| getName      | None                    | String          | Returns the name of the component    |
| setName      | newName: String         | Void            | Sets a new name for the component    |


**Core Logic**:  
- `id` property: Represents the unique identifier of the component, ensuring each component can be uniquely identified.
- `getName` method: Returns the name of the component, providing access to its name.
- `setName` method: Allows setting a new name for the component, enabling modification of the component's name.

### Component/ContentLayoutMode.swift

| Property         | Type           | Description                            |
|------------------|----------------|----------------------------------------|
| contentLayout    | ContentLayoutMode | The layout mode for the component's content. |

| Method                 | Parameter(s)        | Return Type  | Description               |
|------------------------|---------------------|--------------|---------------------------|
| calculateHeight        | None                | CGFloat      | Calculates the height of the content based on the current `ContentLayoutMode`. |
| calculateWidth         | None                | CGFloat      | Calculates the width of the content based on the current `ContentLayoutMode`. |
| calculateSize          | None                | CGSize       | Calculates the size of the content based on the current `ContentLayoutMode`. |

The core logic of this code defines an enumeration `ContentLayoutMode` that specifies how a component's content should be laid out in a collection view. The enumeration includes different layout modes like `fitContainer`, `flexibleHeight`, `flexibleWidth`, and `fitContent`. 

The class or struct that uses this enumeration would have a property `contentLayout` that stores the selected layout mode. Additionally, it provides methods `calculateHeight`, `calculateWidth`, and `calculateSize` to calculate the height, width, and size of the content respectively based on the selected layout mode. These calculations help in determining the dimensions of the content within the parent container.

### Component/Component.swift

| Property              | Type                  | Description                                 |
|-----------------------|-----------------------|---------------------------------------------|
| viewModel             | ViewModel             | Holds the data to be displayed in the component |
| reuseIdentifier        | String                | A unique identifier for reusing the component in a list |
| layoutMode            | ContentLayoutMode     | Represents the layout mode of the content in the component |

| Method                | Parameters            | Return Type        | Description                                 |
|-----------------------|-----------------------|--------------------|---------------------------------------------|
| renderContent         | coordinator: Coordinator | Content          | Creates and configures the initial state of the content |
| render                | content: Content, coordinator: Coordinator | Void | Updates the state of the content with new information |
| layout                | content: Content, container: UIView | Void | Lays out the content within a container view |
| makeCoordinator       | N/A                   | Coordinator        | Creates a coordinator instance for communication purposes |

- 핵심 로직
Component 프로토콜은 UI 프레임워크에서 가장 작은 단위인 컴포넌트를 정의하기 위한 것이다. 이 프로토콜을 구현하면 데이터와 액션을 화면에 선언적으로 표시할 수 있다. `renderContent` 메서드를 통해 초기 상태를 구성하고, `render` 메서드를 사용하여 콘텐츠의 상태를 업데이트한다. `layout` 메서드를 사용하여 콘텐츠를 컨테이너 뷰 내에 레이아웃한다. 또한, `makeCoordinator` 메서드를 구현하여 SwiftUI 인터페이스와의 통신을 위한 Coordinator 인스턴스를 생성할 수 있다.

### Component/AnyComponent.swift

| Property       | Type                            | Description                                                   |
|----------------|---------------------------------|---------------------------------------------------------------|
| `base`         | `some Component`                | Wrapped `Component` whose `ViewModel` is to be type-erased.   |
| `box`          | `any ComponentBox`               | Wraps the underlying `Component` and provides access methods. |
| `reuseIdentifier` | `String`                      | Reuse identifier for the component.                            |
| `layoutMode`   | `ContentLayoutMode`              | Layout mode of the component's content.                        |
| `viewModel`    | `AnyViewModel`                   | Type-erased wrapper for the `Component`'s `ViewModel`.         |

| Method           | Parameters                     | Return Type                        | Description                                                                                   |
|------------------|--------------------------------|------------------------------------|-----------------------------------------------------------------------------------------------|
| `init`           | `base: some Component`         | -                                  | Initializes an `AnyComponent` by wrapping the given `Component`.                               |
| `renderContent`  | `coordinator: Any`             | `UIView`                           | Creates and configures the content object for rendering.                                       |
| `render`         | `content: UIView`, `coordinator: Any` | -                             | Updates the state of the content with new information.                                         |
| `layout`         | `content: UIView`, `container: UIView` | -                           | Lays out the content in the provided container view.                                           |
| `as`             | `(_: T.Type)`                  | `T?`                               | Attempts to downcast the underlying `Component` to the specified type.                           |
| `makeCoordinator`| -                              | `Any`                              | Creates and returns a new `Coordinator` instance for communication between views in SwiftUI.  |
| `==` (static)    | `lhs: AnyComponent`, `rhs: AnyComponent` | `Bool`                        | Compares two `AnyComponent` instances for equality based on their `ViewModel`.                  |

핵심 로직:
- `AnyComponent`는 어떤 `Component`를 wrapping하고, type-erased된 `ViewModel`을 제공하는 구조체이다.
- `ComponentBox` 프로토콜로 기본 `Component`를 wrapping하고 필요한 메소드들을 정의한다.
- `AnyComponentBox`는 `AnyComponent`에 사용되는 구조체로, `ComponentBox` 프로토콜을 구현하고 실제 `Component`와 상호 작용하도록 도와준다.

### Utils/Chunked.swift

| Property              | Type                    | Description                              |
|-----------------------|-------------------------|------------------------------------------|
| base                  | Base                    | The base collection                      |
| chunkCount            | Int                     | The count of elements in each chunk      |
| endOfFirstChunk       | Base.Index              | The end index of the first chunk         |

| Method                              | Parameter          | Return Type     | Description                              |
|-------------------------------------|--------------------|-----------------|------------------------------------------|
| init                                | Base, Int          | Void            | Initialize the ChunksOfCountCollection   |
| startIndex                          | -                  | Index           | Returns the start index                   |
| endIndex                            | -                  | Index           | Returns the end index                     |
| subscript                           | Index              | Element         | Subscript to access elements             |
| index(after:)                       | Index              | Index           | Calculates the next index                |
| index(before:)                      | Index              | Index           | Calculates the previous index            |
| distance(from:to:)                  | Index, Index        | Int             | Calculates the distance between two indexes |
| count                               | -                  | Int             | Returns the total number of chunks       |
| index(_:offsetBy:limitedBy:)        | Index, Int, Index? | Index?          | Offset the index by a given distance     |
| index(_:offsetBy:)                  | Index, Int         | Index           | Offset the index by a given distance     |
| makeOffsetIndex                     | Index, Base.Index, Int, Int, Index?, (Base.Index, Base.Index) -> Bool | Index? | Helper method to calculate offset index |

The ChunksOfCountCollection struct is designed to present the elements of a base collection in chunks of a specified count. The core logic revolves around efficiently splitting the base collection into chunks based on the given count, without creating new storage. The struct uses lazy evaluation to maintain performance, computing the start index upfront to achieve O(1) lookup time. The properties store the base collection, chunk count, and the end index of the first chunk. Methods are provided to access, manipulate, and calculate indexes, as well as to compute the distance between indexes and the total number of chunks. Additionally, methods are implemented to handle offsetting the index by a given distance, taking into account limits and ensuring bounds are not exceeded.

### Utils/Any+Equatable.swift

| 구분    | 이름           | 타입     | 설명                                                         |
|---------|----------------|--------|------------------------------------------------------------|
| Property | other          | Equatable? | 비교 대상을 나타내는 Equatable 타입의 속성                  |
| Method  | isEqual(_: )    | (Equatable) -> Bool | 다른 객체와 동등성 비교하여 결과를 반환하는 메서드        |
| Method  | isExactlyEqual(_: ) | (Equatable) -> Bool | 정확한 동등성 비교를 위한 메서드                       |

**핵심 로직 설명:**
- `isEqual(_:)` 메서드는 다른 객체와의 동등성을 확인하여 `true` 또는 `false`를 반환합니다. 만약 다른 객체가 `Self` 타입이 아닌 경우, `isExactlyEqual(_:)` 메서드를 사용하여 정확한 동등성을 확인합니다.
- `isExactlyEqual(_:)` 메서드는 객체가 정확히 같은 타입이어야만 동등하다고 판단하고, 그렇지 않은 경우 `false`를 반환합니다.

동등성 비교를 하는 과정에서 타입 캐스팅을 통해 객체의 타입을 비교하여 정확한 동등성을 판단할 수 있도록 하는 확장입니다.

### Utils/Collection+SafeIndex.swift

| Property  | Type            | Description                     |
|-----------|-----------------|---------------------------------|
| elements  | Array<Element>  | 저장된 요소들을 관리하는 배열       |
| isEmpty   | Bool            | 배열이 비어있는지 여부를 확인하는 속성 |

| Method          | Parameter       | Return Type  | Description                                 |
|-----------------|-----------------|--------------|---------------------------------------------|
| append(_:)      | Element         | Void         | 배열에 새로운 요소를 추가하는 메서드              |
| remove(at:)     | Index           | Element?     | 주어진 인덱스에 해당하는 요소를 제거하고 반환하는 메서드  |

**핵심 로직 설명:**
- `append(_:)` 메서드는 배열에 새로운 요소를 추가하는 역할을 한다.
- `remove(at:)` 메서드는 주어진 인덱스에 해당하는 요소를 배열에서 제거한 후 제거한 요소를 반환한다. 이때, 안전한 인덱스를 사용하여 인덱스가 배열 범위를 벗어나지 않도록 처리한다.

### Adapter/ComponentSizeStorage.swift

| Property          | Type                | Description                               |
|-------------------|---------------------|-------------------------------------------|
| cellSizeStore     | [AnyHashable: SizeContext] | Dictionary to store the sizes of cells.   |
| headerSizeStore   | [AnyHashable: SizeContext] | Dictionary to store the sizes of headers. |
| footerSizeStore   | [AnyHashable: SizeContext] | Dictionary to store the sizes of footers. |

| Method            | Parameter                           | Return Type           | Description                               |
|-------------------|-------------------------------------|-----------------------|-------------------------------------------|
| cellSize(for:)    | hash: AnyHashable                   | SizeContext?          | Retrieves the size context of a cell.     |
| headerSize(for:)  | hash: AnyHashable                   | SizeContext?          | Retrieves the size context of a header.   |
| footerSize(for:)  | hash: AnyHashable                   | SizeContext?          | Retrieves the size context of a footer.   |
| setCellSize(_:for:)| size: SizeContext, hash: AnyHashable| Void                  | Sets the size context for a cell.         |
| setHeaderSize(_:for:)| size: SizeContext, hash: AnyHashable| Void               | Sets the size context for a header.       |
| setFooterSize(_:for:)| size: SizeContext, hash: AnyHashable| Void                | Sets the size context for a footer.       |

**Core Logic:**
- `ComponentSizeStorageImpl` 클래스는 `ComponentSizeStorage` 프로토콜을 채택하고, cell, header, footer의 크기를 저장하고 검색할 수 있도록 구현한 클래스이다.
- 각각의 크기는 해당하는 타입의 해시 값을 key로 사용하여 Dictionary에 저장한다.
- `cellSizeStore`, `headerSizeStore`, `footerSizeStore`는 각각 cell, header, footer의 크기를 저장하는 딕셔너리 변수이다.
- `cellSize(for:)`, `headerSize(for:)`, `footerSize(for:)`는 각각 cell, header, footer의 크기를 가져오는 메소드이다.
- `setCellSize(_:for:)`, `setHeaderSize(_:for:)`, `setFooterSize(_:for:)`는 각각 cell, header, footer의 크기를 설정하는 메소드이다.
- 이를 통해 각 component의 크기를 저장하고 필요할 때 해당 크기를 검색하거나 저장할 수 있다.

### Adapter/CollectionViewAdapter.swift - part 1

| Property            | Type                        | Description                                            |
|---------------------|-----------------------------|--------------------------------------------------------|
| configuration       | `CollectionViewAdapterConfiguration` | Adapter의 설정(configuration)                          |
| registeredCellReuseIdentifiers | Set<String>           | 등록된 셀 reuseIdentifiers의 집합                         |
| registeredHeaderReuseIdentifiers | Set<String>         | 등록된 헤더 reuseIdentifiers의 집합                       |
| registeredFooterReuseIdentifiers | Set<String>         | 등록된 푸터 reuseIdentifiers의 집합                       |
| collectionView      | UICollectionView?            | 연결된 UICollectionView 객체                             |
| prefetchingIndexPathOperations | [IndexPath: [AnyCancellable]] | 프리페칭 인덱스 경로 연산                                  |
| prefetchingPlugins  | [CollectionViewPrefetchingPlugin] | 프리페칭 플러그인 목록                                 |
| isUpdating          | Bool                        | 데이터 업데이트 중 여부를 나타내는 플래그                   |
| list               | List?                       | 현재 데이터 상태를 나타내는 List                         |
| componentSizeStorage | ComponentSizeStorage      | 컴포넌트 크기 정보를 저장하는 객체                         |
| pullToRefreshControl | UIRefreshControl           | pull-to-refresh 기능을 제공하는 UIRefreshControl 객체   |
| queuedUpdate        | (List, Bool, (() -> Void)?) | 대기 중인 업데이트 정보 (리스트, 애니메이션 여부, 완료 핸들러)   |

| Method                          | Parameters                                     | Return Type  | Description                                      |
|---------------------------------|------------------------------------------------|--------------|--------------------------------------------------|
| init                            | configuration, collectionView, layoutAdapter, prefetchingPlugins | Void   | CollectionViewAdapter 객체를 초기화하는 생성자    |
| apply                           | list, animatingDifferences, completion      | Void         | 데이터를 업데이트하고 UI에 반영하는 메소드              |
| snapshot                        | -                                              | List?        | 현재 데이터 상태를 반환하는 메소드                     |
| registerReuseIdentifiers         | sections                                       | Void         | UICollectionView에 셀, 헤더, 푸터의 reuseIdentifiers 등록 |
| item                            | indexPath                                       | Cell?        | 주어진 IndexPath에 해당하는 Cell을 반환                |
| handleNextBatchIfNeeded          | indexPath                                       | Void         | 다음 배치 핸들링을 처리하는 메소드                      |
| performDifferentialUpdates      | old, new, completion                          | Void         | 차이를 반영하여 UI 업데이트를 수행하는 메소드            |

이 클래스는 UICollectionView와 KarrotListKit의 로직을 연결하는 역할을 수행하는 Adapter로, UICollectionView에 데이터를 업데이트하고 핸들링하는 데 사용됩니다. apply 메소드를 통해 데이터를 업데이트하고 UI에 반영하고, performDifferentialUpdates 메소드를 통해 변경된 내용을 애니메이션으로 표현할 수 있습니다. 또한 RegisterReuseIdentifiers 메소드를 통해 동적으로 셀, 헤더, 푸터의 reuseIdentifiers를 등록하고, 다양한 데이터 핸들링을 처리하는 다양한 메소드를 제공합니다.

### Adapter/CollectionViewAdapter.swift - part 2

| Property                     | Type / Description                                   |
|------------------------------|-------------------------------------------------------|
| list                         | List?                                                 |
| prefetchingIndexPathOperations | [IndexPath: [PrefetchingOperation]]                   |
| prefetchingPlugins            | [PrefetchingPlugin]                                  |
| componentSizeStorage          | ComponentSizeStorage                                 |

| Method                                  | Parameters                                  | Return Type | Description                                                                 |
|-----------------------------------------|---------------------------------------------|-------------|-----------------------------------------------------------------------------|
| scrollViewDidScroll(_: )                | UIScrollView                                | Void        | ScrollView의 스크롤 이벤트를 처리하고 DidScrollEvent 핸들러를 호출함              |
| scrollViewWillBeginDragging(_: )        | UIScrollView                                | Void        | ScrollView의 드래깅 시작 이벤트를 처리하고 WillBeginDraggingEvent 핸들러를 호출함 |
| scrollViewWillEndDragging(_:with:targetContentOffset:) | UIScrollView, CGPoint, UnsafeMutablePointer<CGPoint> | Void | ScrollView의 드래깅 끝 이벤트를 처리하고 WillEndDraggingEvent 핸들러를 호출함    |
| collectionView(_:prefetchItemsAt:)       | UICollectionView, [IndexPath]               | Void        | CollectionView에 prefetching을 처리하고 PrefetchingOperation을 생성함           |
| collectionView(_:cancelPrefetchingForItemsAt:) | UICollectionView, [IndexPath]          | Void        | CollectionView의 prefetching을 취소하고 PrefetchingOperation을 취소함          |
| numberOfSections(in:)                   | UICollectionView                             | Int         | CollectionView의 섹션 개수를 반환함                                             |
| collectionView(_:numberOfItemsInSection:) | UICollectionView, Int                         | Int         | 주어진 섹션의 아이템 개수를 반환함                                               |
| collectionView(_:cellForItemAt:)          | UICollectionView, IndexPath                  | UICollectionViewCell | CollectionView의 아이템 Cell을 반환하고 화면에 렌더링함                           |
| collectionView(_:viewForSupplementaryElementOfKind:at:) | UICollectionView, String, IndexPath | UICollectionReusableView | CollectionView의 보조 요소를 반환하고 화면에 렌더링함         |

이 코드는 UICollectionView를 처리하는 CollectionViewAdapter 클래스에 대한 확장을 보여줍니다. 주요 기능은 scrollView 이벤트 처리, prefetching 기능, 데이터 소스 관련 메서드로 섹션과 아이템의 개수를 반환하고 Cell, Header, Footer 뷰를 렌더링하는 것입니다. prefetchingIndexPathOperations 딕셔너리를 사용하여 prefetching 작업을 추적하고 처리하며, componentSizeStorage를 통해 Cell, Header, Footer의 크기를 관리합니다.scrollViewDidScroll(_: ), collectionView(_:prefetchItemsAt:), collectionView(_:cancelPrefetchingForItemsAt:)와 같은 메서드는 각각 scrollView의 스크롤 이벤트, prefetching 이벤트를 처리하고 각각에 대한 핸들러를 호출합니다. 각 메서드는 CollectionViewAdapter가 CollectionView와 상호작용하는 방식을 제공하고 효율적인 데이터 소스 구현을 지원합니다.

### Adapter/CollectionViewAdapterConfiguration.swift

| 구성요소 | 속성 및 메서드 | 타입/파라미터/리턴 타입 | 설명 |
|---------|----------------|----------------------|------|
| CollectionViewAdapterConfiguration | refreshControl | RefreshControl | CollectionView의 RefreshControl을 설정합니다. |
| CollectionViewAdapterConfiguration | batchUpdateInterruptCount | Int | 배치 업데이트가 대체되는 최대 ChangeSet 개수를 나타냅니다. |
| CollectionViewAdapterConfiguration | init | refreshControl: RefreshControl, batchUpdateInterruptCount: Int | CollectionViewAdapterConfiguration 인스턴스를 초기화합니다. |
| CollectionViewAdapterConfiguration.RefreshControl | isEnabled | Bool | RefreshControl이 활성화되었는지 나타냅니다. |
| CollectionViewAdapterConfiguration.RefreshControl | tintColor | UIColor | RefreshControl의 틴트 색상을 나타냅니다. |
| CollectionViewAdapterConfiguration.RefreshControl | enabled | tintColor: UIColor -> RefreshControl | RefreshControl을 활성화하고 틴트 색상을 설정하는 메서드입니다. |
| CollectionViewAdapterConfiguration.RefreshControl | disabled | () -> RefreshControl | RefreshControl을 비활성화하는 메서드입니다. |

**핵심 로직 설명**:
- `refreshControl` 속성은 CollectionView의 RefreshControl을 설정하고, `batchUpdateInterruptCount` 속성은 배치 업데이트가 언제 대체될지를 결정합니다.
- `CollectionViewAdapterConfiguration`의 초기화 메서드를 통해 설정을 포함한 인스턴스를 생성할 수 있습니다.
- `RefreshControl` 구조체는 RefreshControl의 활성화 여부와 색상을 관리합니다.
- `enabled` 메서드는 RefreshControl을 활성화하고 색상을 설정하며, `disabled` 메서드는 RefreshControl을 비활성화합니다.

### Adapter/CollectionViewLayoutAdaptable.swift

|| Property         | Type                         | Description                                         ||
||-----------------|------------------------------|-----------------------------------------------------||
|| dataSource      | CollectionViewLayoutAdapterDataSource? | 데이터 소스로 NSCollectionLayoutSection을 생성하기 위해 필요한 정보를 제공하는 프로토콜 데이터 소스   ||

||-          | -                            | -                                                   ||
|| Method           | Parameter(s)                 | Return Type                  | Description                                         ||
||-----------------|------------------------------|-----------------------------|-----------------------------------------------------||
|| sectionItem     | index: Int                  | Section?                    | 주어진 인덱스의 섹션 아이템을 반환하는 메소드                       ||

### 핵심로직 설명
1. `CollectionViewLayoutAdapter` 클래스는 `CollectionViewLayoutAdaptable` 프로토콜을 구현한 기본 구현체이며, UICollectionView의 레이아웃을 처리하는 역할을 한다.
2. `sectionLayout` 메소드는 주어진 인덱스와 레이아웃 환경을 기반으로 NSCollectionLayoutSection을 생성해 반환한다.
3. `sectionItem` 메소드는 주어진 인덱스에 해당하는 섹션 아이템을 반환해주는 역할을 한다.
4. 필요한 데이터 소스를 주입받아 해당 데이터를 활용하여 NSCollectionLayoutSection을 생성하고 반환한다.

### NextBatchTrigger/NextBatchContext.swift

| Property      | Type           | Description                               |
|---------------|----------------|-------------------------------------------|
| state         | NextBatchContext.State  | Represents the state for the next batch trigger |

| Method        | Parameter      | Return Type   | Description                               |
|---------------|----------------|---------------|-------------------------------------------|
| init          | state: NextBatchContext.State = .pending  | NextBatchContext   | Initializes a NextBatchContext instance with the provided state. |

The NextBatchContext struct represents the context about the next batch trigger, which has a property `state` to store the state of the trigger (pending or triggered). The struct has an initializer method `init` to create a new instance of NextBatchContext with an initial state. In this case, `state` property is of type `NextBatchContext.State`.

The core logic of this struct revolves around maintaining the state of the next batch trigger, allowing the developer to track whether the trigger has been pending or has occurred. The struct encapsulates this information in a clear and concise manner, making it easy to manage and change the state as needed.

### NextBatchTrigger/NextBatchTrigger.swift

| Property      | Type             | Description                               |
|---------------|------------------|-------------------------------------------|
| threshold     | Int              | Threshold value for triggering the event  |
| context       | NextBatchContext | Current state for next batch trigger      |
| handler       | Closure           | Closure called when trigger occurs        |

| Method        | Parameter                  | Return Type | Description                                                                                             |
|---------------|----------------------------|-------------|---------------------------------------------------------------------------------------------------------|
| init          | threshold: Int,             |             | Initializes a NextBatchTrigger object with the specified threshold value, initial context, and handler |
|               | context: NextBatchContext,  |             |                                                                                                         |
|               | handler: Closure            |             |                                                                                                         |

Core Logic:
- `NextBatchTrigger` 클래스는 페이징 기능을 구현하는데 사용되는 `NextBatchTrigger`를 제공합니다.
- `threshold` 값이 현재 표시된 콘텐츠의 인덱스와 마지막 콘텐츠의 인덱스의 차이보다 크거나 같으면 트리거가 발생합니다.
- `handler` 클로저는 트리거가 발생했을 때 호출되는 함수를 나타냅니다.

### View/UICollectionViewComponentCell.swift

| Property                | Type          | Description                                      |
|-------------------------|---------------|--------------------------------------------------|
| renderedContent         | UIView?       | 렌더링된 콘텐츠를 나타내는 UIView                    |
| coordinator             | Any?          | 셀의 코디네이터 객체                              |
| renderedComponent       | AnyComponent? | 렌더링된 컴포넌트를 나타내는 AnyComponent 객체         |
| cancellables            | [AnyCancellable]? | Combine 라이브러리의 데이터 스트림 구독 객체들의 배열 |
| onSizeChanged           | ((CGSize) -> Void)? | 셀의 크기가 변경될 때 호출되는 클로저                |

| Method                                | Parameters                | Return Type | Description                                      |
|---------------------------------------|---------------------------|-------------|--------------------------------------------------|
| init(frame:)                          | CGRect                    | Void        | 셀을 주어진 프레임으로 초기화하는 메서드              |
| prepareForReuse                       | -                         | Void        | 셀을 재사용하기 전에 호출되는 메서드                   |
| preferredLayoutAttributesFitting(_:)  | UICollectionViewLayoutAttributes | UICollectionViewLayoutAttributes | 셀의 크기를 콘텐츠에 맞게 조정하는 메서드 |

이 클래스는 UICollectionViewCell을 상속하며, ComponentRenderable 프로토콜을 구현하는 UICollectionViewComponentCell을 정의합니다. 이 셀은 렌더링된 콘텐츠, 코디네이터, 렌더링된 컴포넌트, 데이터 스트림 구독 객체 배열 등을 포함하고 있습니다.

주요 메서드인 `preferredLayoutAttributesFitting(_:)`에서는 셀의 크기를 콘텐츠의 크기에 맞게 조정하고, 이때 콘텐츠의 크기가 변경될 때 `onSizeChanged` 클로저를 호출하여 외부에 크기 변경을 알립니다.

### View/UICollectionComponentReusableView.swift

| Property           | Type                 | Description                                        |
|--------------------|----------------------|----------------------------------------------------|
| renderedContent    | UIView?              | The content that will be rendered in the view.     |
| coordinator         | Any?                   | Coordinator object for managing the component.    |
| renderedComponent | AnyComponent?   | The component to be rendered in the view.         |
| onSizeChanged     | ((CGSize) -> Void)? | Closure to be called when the size changes.      |

| Method                                                | Parameters                   | Return Type | Description                                      |
|------------------------------------------------------|------------------------------|-------------|--------------------------------------------------|
| init(frame: CGRect)                               | frame: CGRect             |              | Initializes the view with the given frame.    |
| preferredLayoutAttributesFitting(_)  | layoutAttributes: UICollectionViewLayoutAttributes | UICollectionViewLayoutAttributes | Calculates and returns the layout attributes for the view based on the rendered content's size. Updates the frame size and calls the `onSizeChanged` closure if the rendered component exists. |

- `UICollectionComponentReusableView` 클래스는 `UICollectionReusableView`를 상속받고, `ComponentRenderable` 프로토콜을 준수합니다.
- `renderedContent`는 렌더링할 내용을 나타내는 `UIView` 객체를 저장합니다.
- `coordinator`는 컴포넌트를 관리하는 `Any` 타입의 객체를 나타냅니다.
- `renderedComponent`는 뷰에 렌더링할 컴포넌트를 저장합니다.
- `onSizeChanged`는 크기 변경 시 호출될 클로저를 저장합니다.
- `preferredLayoutAttributesFitting(_:)` 메서드는 주어진 레이아웃 속성을 기반으로 렌더링된 컨텐츠의 크기를 계산하고 레이아웃 속성을 반환합니다. 렌더링된 컴포넌트가 있는 경우, 크기 변경 클로저를 호출하고 프레임 크기를 업데이트합니다.

### View/ComponentRenderable.swift

| Property           | Type                | Description                                    |
|--------------------|---------------------|------------------------------------------------|
| componentContainerView | UIView              | Rendered component를 포함하는 뷰의 컨테이너 역할                 |
| renderedContent        | UIView?             | 렌더링된 컨텐츠를 저장하는 프로퍼티                      |
| coordinator            | Any?                | 컴포넌트 간의 상호작용을 조정하는 코디네이터 프로퍼티               |
| renderedComponent      | AnyComponent?       | 현재 렌더링된 컴포넌트를 저장하는 프로퍼티                 |

| Method           | Parameter                                      | Return Type   | Description                                          |
|------------------|------------------------------------------------|---------------|------------------------------------------------------|
| render           | component: AnyComponent                        | Void         | 주어진 컴포넌트를 렌더링하고 내부 상태를 업데이트하는 메서드      |
| renderContent    | coordinator: Any                               | UIView        | 주어진 코디네이터를 활용하여 컨텐츠를 렌더링하는 메서드          |
| layout           | content: UIView, in container: UIView          | Void         | 렌더링된 컨텐츠를 주어진 컨테이너에 배치하는 메서드              |
| makeCoordinator  | None                                           | Any           | 현재 컴포넌트에 해당하는 새로운 코디네이터를 생성하는 메서드          |

해당 코드는 `ComponentRenderable` 프로토콜을 정의하고, 이를 채택하는 클래스나 구조체에서 필요한 동작을 정의한 것입니다. 이 프로토콜은 렌더링이 가능한 컴포넌트를 다룰 때 사용됩니다. `render` 메서드를 통해 컴포넌트를 렌더링하고, 내부 상태를 업데이트합니다. `renderContent` 메서드는 주어진 코디네이터를 활용하여 컨텐츠를 렌더링하고, `layout` 메서드는 해당 컨텐츠를 주어진 컨테이너에 배치합니다. `makeCoordinator` 메서드는 현재 컴포넌트에 해당하는 새로운 코디네이터를 생성합니다.

### Builder/SectionsBuilder.swift

| 구분   | 이름       | 타입         | 설명                                       |
|--------|------------|--------------|--------------------------------------------|
| Property | resultBuilder | Result Builder | Section 배열을 반환하는 Result Builder 구조체 |
| Method   | buildBlock  | (Section...) -> [Section] | 주어진 Section을 블록에 묶어 배열로 반환 |
| Method   | buildBlock  | ([Section]...) -> [Section] | 주어진 Section 배열을 블록에 묶어 하나의 배열로 반환 |
| Method   | buildBlock  | ([Section]) -> [Section] | 주어진 Section 배열을 그대로 반환 |
| Method   | buildOptional | ([Section]?) -> [Section] | Optional Section 배열을 반환하며, nil일 경우 빈 배열을 반환 |
| Method   | buildEither | (first: [Section]) -> [Section] | 첫 번째 Section 배열을 반환 |
| Method   | buildEither | (second: [Section]) -> [Section] | 두 번째 Section 배열을 반환 |
| Method   | buildExpression | (Section...) -> [Section] | 주어진 Section을 배열로 반환 |
| Method   | buildExpression | ([Section]...) -> [Section] | 주어진 Section 배열을 배열로 변환 |
| Method   | buildArray  | ([[Section]]) -> [Section] | 2차원 Section 배열을 1차원 배열로 변환 |

**핵심 로직 설명:**
- `resultBuilder`는 Swift의 `@resultBuilder` 속성을 활용하여 Section 배열을 관리하는 구조체이다.
- 주요 메소드인 `buildBlock`는 주어진 Section 배열을 블록에 묶어 하나의 배열로 반환한다.
- `buildOptional`은 Optional Section 배열을 반환하며, nil일 경우 빈 배열을 반환한다.
- `buildEither` 메소드는 두 가지 선택지 중 하나의 Section 배열을 반환한다.
- 나머지 메소드들은 주어진 Section을 배열로 변환하거나 2차원 배열을 1차원 배열로 변환하는 역할을 한다.

### Builder/CellsBuilder.swift

| 구성 요소 | 이름 | 타입 | 설명 |
|--------------|---------|--------|----------|
| Property | components | [Cell] | CellsBuilder에 전달되는 요소를 배열로 저장하는 프로퍼티 |
| Method | buildBlock | (Cell...) -> [Cell] | 주어진 Cell들을 블록 단위로 묶어 배열로 반환하는 메서드 |
| Method | buildOptional | ([Cell]?) -> [Cell] | 옵셔널한 Cell 배열을 받아서 값이 존재하면 반환하고, 그렇지 않으면 빈 배열을 반환하는 메서드 |
| Method | buildEither | (first: [Cell]) -> [Cell] | 첫 번째 Cell을 받아 반환하는 메서드 |
| Method | buildEither | (second: [Cell]) -> [Cell] | 두 번째 Cell을 받아 반환하는 메서드 |
| Method | buildExpression | (Cell...) -> [Cell] | 표현식 Cell들을 받아 반환하는 메서드 |

**핵심 로직 설명:**
`CellsBuilder`는 `resultBuilder`로 정의된 열거형이며, 배열 형태의 `Cell` 요소들을 묶어주는 역할을 합니다. 내부에는 다양한 형태의 빌더 메서드가 구현되어 있어 각각의 형태에 맞게 `Cell` 요소를 처리하고 적절히 반환합니다. 이를 통해 각종 빌더 메서드를 사용하여 `Cell`들을 효율적으로 처리하고 배열로 반환할 수 있습니다.

### Event/ListingViewEvent.swift

| Property           | Type           | Description                                |
|-------------------|----------------|--------------------------------------------|
| id                | AnyHashable    | Event의 고유 식별자                           |

| Method              | Parameter         | Return Type      | Description                                      |
|---------------------|-------------------|------------------|--------------------------------------------------|
| id ()               | -                 | AnyHashable      | Event의 고유 식별자를 반환                         |
| handler (Input)     | Input             | Output           | 입력값을 받아 처리하고 결과를 반환하는 핸들러 메서드 |

**핵심 로직**
- ListingViewEvent 프로토콜은 제네릭을 사용하여 Input 타입과 Output 타입을 연결하고 있습니다.
- 프로토콜 내부에는 고유 식별자인 id와 입력값을 처리하여 출력값을 반환하는 핸들러 메서드인 handler가 정의되어 있습니다.
- Default Implementation에서는 id를 구현하여 String(reflecting: Self.self) 을 통해 Event 타입의 이름을 고유 식별자로 사용하도록 설정하고 있습니다.

### Event/ListingViewEventHandler.swift

| Property             | Type                           | Description                                 |
|----------------------|--------------------------------|---------------------------------------------|
| eventStorage         | ListingViewEventStorage        | Store events registered by the event handler|

| Method              | Parameter                      | Return Type           | Description                                 |
|---------------------|--------------------------------|-----------------------|---------------------------------------------|
| registerEvent       | event: ListingViewEvent         | Self                  | Register an event with the event handler    |
| event               | type: E.Type                    | E?                    | Retrieve an event of a specific type        |

핵심 로직:
ListingViewEventHandler 프로토콜을 채택하는 클래스나 구조체는 이벤트 관련 동작을 처리하기 위해 선언된 프로퍼티와 메소드를 사용할 수 있습니다. eventStorage는 이벤트를 저장하고 관리하는 ListingViewEventStorage 타입의 프로퍼티입니다. registerEvent 메소드를 통해 이벤트를 등록하고, event 메소드를 통해 특정 타입의 이벤트를 가져올 수 있습니다. eventStorage를 통해 등록된 이벤트를 관리하고 필요에 따라 적절한 이벤트를 가져와 처리할 수 있습니다.

### Event/ListingViewEventStorage.swift

| Property       | Type               | Description                                      |
|----------------|--------------------|--------------------------------------------------|
| source         | [AnyHashable: Any] | 이벤트를 저장하는 딕셔너리                         |

| Method                  | Parameter          | Return Type    | Description                                                                                  |
|-------------------------|--------------------|----------------|----------------------------------------------------------------------------------------------|
| event(for:)             | type: E.Type       | E?             | 주어진 이벤트 타입에 대한 이벤트를 반환한다.                                                      |
| register(_)             | event: ListingViewEvent | Void           | 주어진 이벤트를 딕셔너리에 등록한다.                                                               |

이 클래스는 ListingViewEvent를 저장하는 딕셔너리 속성 'source'와 이벤트를 반환하거나 등록하는 두 가지 메서드로 구성되어 있습니다. 'event(for:)' 메서드는 주어진 이벤트 타입에 해당하는 이벤트를 반환하고, 'register(_)' 메서드는 주어진 이벤트를 딕셔너리에 등록합니다. 딕셔너리를 사용하여 이벤트를 효율적으로 저장하고 관리할 수 있도록 설계되었습니다.

### Event/Cell/DidSelectEvent.swift

| Property       | Type                    | Description                             |
|----------------|-------------------------|-----------------------------------------|
| handler        | Closure `(EventContext) -> Void` | A closure that handles the selection event. |

| Method                  | Parameter                       | Return Type | Description                                                                        |
|----------------------|----------------------------------|-------------|------------------------------------------------------------------------------------|
| `callHandler(with:)` | `eventContext: EventContext`     | `Void`      | Calls the closure handler with the provided event context to handle the selection. |

본 코드는 `DidSelectEvent` 구조체를 정의하고, 선택 이벤트 정보를 캡슐화하며 선택 이벤트를 처리하는 클로저 객체를 포함합니다. 
`DidSelectEvent` 구조체는 `ListingViewEvent` 프로토콜을 채택하고 있습니다. 
`EventContext` 내부 구조체는 선택된 셀의 인덱스 경로 및 해당 셀이 소유한 컴포넌트를 저장합니다.
`handler` 클로저는 셀이 선택될 때 호출되는 클로저로, `eventContext`를 매개변수로 받아 선택 이벤트를 처리합니다.
`callHandler(with:)` 메서드는 클로저 핸들러를 제공된 이벤트 컨텍스트로 호출하여 선택 이벤트를 처리하는데 사용됩니다.

### Event/Common/WillDisplayEvent.swift

| Property         | Type               | Description                                                             |
|------------------|--------------------|-------------------------------------------------------------------------|
| handler          | `(EventContext) -> Void`  | The closure called when the view is being added.                       |

| Method           | Parameter(s)       | Return Type          | Description                                                             |
|------------------|--------------------|----------------------|-------------------------------------------------------------------------|
| `EventContext`   | `indexPath: IndexPath`, `anyComponent: AnyComponent`, `content: UIView?` | - | Initializer for the `EventContext` struct.                      |


### Core Logic:
이 코드는 `WillDisplayEvent` 구조체를 정의하고, `handler` 클로저를 포함한다. `WillDisplayEvent`는 `ListingViewEvent` 프로토콜을 준수하는 구조체이며, `EventContext` 구조체는 `willDisplayEvent` 이벤트의 정보를 캡슐화한다. `handler` 클로저는 뷰가 추가될 때 호출되며, 추가되는 뷰와 관련된 작업을 처리한다.

### Event/Common/DidEndDisplayingEvent.swift

|          Property         |       Type        |              Description               |
|---------------------------|-------------------|----------------------------------------|
|        `handler`          |    `(EventContext) -> Void`    |    Closure that is called when the view is removed.    |

|          Method           |       Parameters       |       Return Type       |              Description               |
|---------------------------|------------------------|-------------------------|----------------------------------------|
|          `EventContext`             |    `indexPath: IndexPath, anyComponent: AnyComponent, content: UIView?`    |    -    |    Represents the context information of the didEndDisplaying event, including the index path of the removed view, the component owned by the view, and the content of the view.    |

### 핵심 로직
이 코드는 `DidEndDisplayingEvent` 구조체를 정의하여 `didEndDisplaying` 이벤트 정보를 캡슐화하고, 이벤트를 처리하는 클로저 핸들러를 포함하고 있다. `handler` 프로퍼티는 뷰가 제거될 때 호출되는 클로저를 저장한다. 또한 `EventContext` 내부 구조체는 뷰가 제거된 이벤트에 대한 상세 정보를 포함하는데, 제거된 뷰의 인덱스 경로, 뷰가 소유한 컴포넌트 및 컨텐츠를 포함한다.

### Event/List/DidScrollEvent.swift

| 구성 요소   | 종류 및 타입               | 설명                                 |
|---------------|----------------------------|-------------------------------------|
| Property      | `handler: (EventContext) -> Void` | 스크롤 이벤트를 처리하는 클로저            |

| Method                          | Parameter                         | Return Type      | 설명                               |
|---------------------------------|-----------------------------------|-------------------|-----------------------------------|
| `scrollEvent(_: EventContext)`  | `context: EventContext`           | `Void`            | 사용자가 컨텐츠 뷰를 스크롤할 때 호출되는 메서드        |

### 핵심 로직
`DidScrollEvent` 구조체는 스크롤 이벤트 정보를 캡슐화하고, 스크롤 이벤트를 처리하는 클로저를 포함합니다. 사용자가 collectionView 내부의 컨텐츠 뷰를 스크롤할 때 `handler` 클로저가 호출되어 이벤트를 처리합니다. 클로저에는 `EventContext` 구조체가 전달되는데, 이는 스크롤 이벤트가 발생한 collectionView에 대한 정보를 포함합니다.

### Event/List/WillBeginDraggingEvent.swift

| 구조체(Struct) WillBeginDraggingEvent |
|--------------------------------------|----------------------|
| Property:                            | Type:                |
| handler                              | Closure (EventContext) -> Void |
|                                      |                      |
| Method:                              | Parameter:           | Return Type: |
| init(handler:)                       | handler: Closure (EventContext) -> Void | - |

간단한 설명:
- `WillBeginDraggingEvent` 구조체는 `will begin dragging` 이벤트 정보를 캡슐화하고 이를 처리하는 closure 객체를 포함한다.
- `EventContext` 구조체는 `collectionView` 객체를 저장하고 있다.

핵심 로직:
- `WillBeginDraggingEvent` 구조체는 `ListingViewEvent` 프로토콜을 채택하고, `collectionView`가 컨텐츠 뷰를 스크롤하기 직전에 호출될 클로저를 포함한다.

### Event/List/PullToRefreshEvent.swift

| 구성 요소    | Type                | 설명                                      |
|-------------|---------------------|------------------------------------------|
| handler     | Closure             | 사용자가 새로고침을 요청했을 때 호출되는 클로저 |

| 메서드      | Parameter            | Return Type           | 설명                             |
|------------|----------------------|----------------------|-----------------------------------|
| handle     | EventContext         | Void                 | 새로고침 이벤트를 처리하는 메서드 |

이 코드는 `PullToRefreshEvent` 구조체를 정의하고, `handler` 클로저를 포함하여 사용자의 새로고침 이벤트를 처리하는 기능을 제공합니다. 사용자가 새로고침을 요청하면 `handler` 클로저가 호출됩니다. 핵심 로직은 사용자의 새로고침 요청을 감지하고 처리하는 것이며, 이를 위해 `handler` 클로저를 사용합니다.

### Event/List/WillEndDraggingEvent.swift

| Property           | Type                           | Description                                                      |
|--------------------|--------------------------------|------------------------------------------------------------------|
| collectionView      | UICollectionView                 | The collectionView object where the user ended the touch.        |
| velocity           | CGPoint                        | The velocity of the collectionView at the moment touch was released. |
| targetContentOffset| UnsafeMutablePointer<CGPoint>  | The expected offset when scrolling action decelerates to a stop. |

| Method            | Parameters                            | Return Type | Description                                                                                                                            |
|-------------------|---------------------------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------|
| handler           | EventContext                          | Void        | A closure that's called when the user finishes scrolling the content. Receives EventContext object as parameter for handling the event.  |

**Core Logic:**
- 구조체 `WillEndDraggingEvent`는 `ListingViewEvent` 프로토콜을 채택한 구조체이다.
- `WillEndDraggingEvent` 구조체 내부에는 `EventContext` 내부 구조체와 `handler` 클로저가 포함되어 있다.
- `EventContext` 구조체는 사용자가 터치를 끝낼 때의 정보를 캡슐화하며, collectionView, velocity, targetContentOffset 세 가지 프로퍼티를 가지고 있다.
- `handler` 클로저는 사용자가 콘텐츠 스크롤링을 마칠 때 호출되는 클로저로, `EventContext` 객체를 매개변수로 받아 이벤트를 처리한다.

