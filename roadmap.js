/* Purpose:
 *
 * This file provides a mechanism for inserting roadmap slides with an 'active'
 * element automatically highlighted.
 *
 * Copyright (C) 2020, Henrik Laxhuber
 **/

export default () => {
  return {
    id: "roadmap",
    init: instance => {
      const config = instance.getConfig().roadmap;
      if (!config || !config.roadmap || !config.title) {
        console.error("roadmap configuration invalid.");
        return;
      }
      document
        .querySelectorAll("section[data-roadmap]")
        .forEach((slide, idx) => {
          console.log("hi");

          if (idx == 0) {
            // initial overview slide
            var title = document.createElement("h3");
            title.innerHTML = config.title;
            slide.appendChild(title);

            var list = document.createElement("ul");
            config.roadmap.forEach(item => {
              var li = document.createElement("li");
              li.innerHTML = item;
              li.classList.add("fragment");
              list.appendChild(li);
            });
            slide.appendChild(list);
          } else {
            // 'active' element slide
            var title = document.createElement("h3");
            title.innerHTML = config.title;
            slide.appendChild(title);

            var list = document.createElement("ul");
            config.roadmap.forEach((item, item_idx) => {
              var li = document.createElement("li");
              li.innerHTML = item;
              if (item_idx == idx - 1) li.classList.add("active");
              else li.classList.add("hidden");
              list.appendChild(li);
            });
            slide.appendChild(list);
          }
        });
    }
  };
};
