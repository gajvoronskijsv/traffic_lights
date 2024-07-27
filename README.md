<h1 class="code-line" data-line-start=0 data-line-end=1>
  <a id="____0"></a>Адаптивный алгоритм работы светофоров
</h1>
<p class="has-line-data" data-line-start="2" data-line-end="4">Абстракции светофоров и окружения сформированы так, чтобы соответствовать <a href="https://docs.yandex.ru/docs/view?url=ya-disk-public%3A%2F%2FoHjlRzVV3Vli6skj5jT4W1x8y7udgo%2ByccMra5WIF2WfPfWeehGtd3LRx4jkgpmiLnwuG65u%2BCaUWt4uUumLKA%3D%3D&amp;name=%D0%A2%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%B5_%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82.docx">тз</a>. <br> Для запуска достаточно выполнить traffic_lights.py интерпретатором Python 3.11. Можно переключить режим работы генератора трафика путем комента/раскомента строк в конце скрипта.</p>
<h4 class="code-line" data-line-start=7 data-line-end=8>
  <a id="__7"></a>Описание алгоритма
</h4>
<ul>
  <li class="has-line-data" data-line-start="9" data-line-end="10">Перекресток, симулируемый классом Crossroad, создает светофоры и запускает генерацию трафика. С периодичностью в 5 секунд в консоль выводится текущее состояние перекрестка до и после работы светофоров Позиция пары значений (g/r)(N) соответствует позициям светофоров на иллюстрации к тз, где g - зеленый свет, r - красный свет, N - величина трафика, который видит камера перед светофором.</li>
  <li class="has-line-data" data-line-start="10" data-line-end="11">Алгоритм может использовать произвольное количество схем движения на перекрестке, описываемых классом MovementScheme.</li>
  <li class="has-line-data" data-line-start="11" data-line-end="13">Каждый светофор описывается классом TrafficLight и работает асинхронно. Светофор общается с остальными светофорами на перекрестке сообщениями (класс Event), которые передаются средой (классом Crossroad). Светофоры знают какие схемы движения есть на перекрестке и в каких он участвует. За счет совместного выбора схемы, светофоры решают, какое состояние они примут в следующую очередь.</li>
</ul>
<p class="has-line-data" data-line-start="13" data-line-end="14">Цикл работы светофора в рамках схемы движения следующий:</p>
<ul>
  <li class="has-line-data" data-line-start="15" data-line-end="16">Светофор отправляет свой Event остальным и ожидает, пока остальные светофоры также пришлют свой Event. В этом сообщении указывается, голосует ли данный светофор за схему движения в данный момент (“vote”), или уступает остальным светофорам на перекрестке (“pass”). Также в сообщении указывается величина очереди с камеры светофора.</li>
  <li class="has-line-data" data-line-start="16" data-line-end="17">Получив все Event, светофор подставляет данные из них в схемы движения на перекрестке, формируя рейтинг схемы. Положительная часть рейтинга формируется из суммарной загрузки всех светофоров, которые включат зеленый свет при работе этой схемы (то есть отражает то, сколько единиц транспорта и людей схема может пропустить), но только если светофор в сообщении не указывает, что уступает остальным. Отрицательная часть рейтинга формируется из суммарной загрузки всех светофоров, которые включат красный, также при условии, что эти светофоры не уступают остальным.</li>
  <li class="has-line-data" data-line-start="17" data-line-end="18">Получив все рейтинги схем, светофор проверяет, не уступают ли все светофоры на перекрестке одновременно. Это может означать, что каждый светофор уже пропустил свой трафик и нужно сбросить очередь. Также это может означать, что ни у одного светофора нет трафика на камере. Если все светофоры уступают, то светофор решает, хочет ли он включаться, в зависимости от трафика на своей камере, и заново отсылает свой Event на голосование.</li>
  <li class="has-line-data" data-line-start="18" data-line-end="20">Если не все светофоры уступают и произошел выбор лучшей схемы, светофор переключает свое состояние, чтобы соответствовать схеме. Если светофор включил зеленый свет, то значит что он пропустит свой трафик и начнет уступать другим светофорам, отправив в следующем сообщении “pass”. Следующее сообщение, которое инициирует очередной цикл голосования, он отправит с задержкой в 5 секунд.</li>
</ul>
<h4 class="code-line" data-line-start=20 data-line-end=21>
  <a id="__20"></a>Преимущества алгоритма
</h4>
<ul>
  <li class="has-line-data" data-line-start="22" data-line-end="23">Если нет трафика перед светофором, он не будет влиять на оптимальную схему движения.</li>
  <li class="has-line-data" data-line-start="23" data-line-end="24">Если трафик есть, то победит та схема, которая в теории пропустит за цикл больше единиц транспорта и людей.</li>
  <li class="has-line-data" data-line-start="24" data-line-end="25">При этом исключена ситуация, когда светофоры зациклятся между двумя самыми нагруженными трафиком схемами, благодаря системе уступок. Гарантровано, что каждый участник движения дождется своей очереди.</li>
  <li class="has-line-data" data-line-start="25" data-line-end="27">Можно добавить любое количество схем движения.</li>
</ul>
<h4 class="code-line" data-line-start=27 data-line-end=28>
  <a id="_______27"></a>Что можно улучшить после отправки рабочей версии
</h4>
<ul>
  <li class="has-line-data" data-line-start="29" data-line-end="30">Лучше структурировать/закоментровать код.</li>
  <li class="has-line-data" data-line-start="30" data-line-end="31">Расширить функционал генератора трафика и протестировать экзотические сценарии.</li>
  <li class="has-line-data" data-line-start="31" data-line-end="32">Симулировать время переключения с желтого на красный</li>
  <li class="has-line-data" data-line-start="32" data-line-end="33">Добавить время для очистки перекрестка перед включением следующей схемы</li>
  <li class="has-line-data" data-line-start="33" data-line-end="35">Добавить динамическое изменение времени работы светофоров в выбранной схеме в зависимости от трафика</li>
</ul>