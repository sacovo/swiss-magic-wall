
const Info = {
  data() {
    return {
      canton_id: 0,
      commune_id: 0,
      canton_json: {},
      commune_json: {},
      active: false,
      commune_active: false,
    };
  },
  methods: {
    selectCanton(canton_id) {
      this.canton_id = canton_id;
      this.commune_active = false;
      this.active = true;
    },

    deselectCanton() {
      this.canton_id = 0;
      this.commune_active = false;
      this.active = false;
    },

    selectCommune(commune_id) {
      this.commune_id = commune_id;
      this.commune_active = true;
    },

    getCanton() {
      return this.canton_json[this.canton_id];
    },

    styleWidth(p) {
      return `width:${p}%`;
    },

    stylePercent(p) {
      return numeral(p).format('0.0');
    }

  },

  computed: {
    canton() {
      return this.getCanton();
    },
    canton_image() {
      return `/static/icons/kantone/${this.canton_id}.svg`;
    },
    open() {
      let canton = this.getCanton();
      return canton.total > canton.counted;
    },
    progress() {
      let canton = this.getCanton();
      return (canton.yes_counted + canton.no_counted) / canton.total_votes * 100;
    },
    commune() {
      return this.commune_json[this.commune_id];
    },
    canton_yes_c() {
      let canton = this.getCanton();
      return canton.yes_counted / canton.total_votes * 100 ;
    },
    canton_yes_p() {
      let canton = this.getCanton();
      return canton.yes_predicted / canton.total_votes * 100 ;
    },
    canton_no_p() {
      let canton = this.getCanton();
      return canton.no_predicted / canton.total_votes * 100 ;

    },
    canton_no_c() {
      let canton = this.getCanton();
      return canton.no_counted / canton.total_votes * 100 ;
    },
    commune_yes() {
      return this.commune_json[this.yes_percent] ;

    },
    commune_no() {
      return this.commune_json[this.no_percent] ;
    },
  }
};

window.addEventListener('load', (event) => {


  const vm = Vue.createApp(Info).mount('#cantonInfo')

  let votationMaps = document.getElementsByClassName('VotationMap');
  console.log("Hello");

  for (var i = 0; i < votationMaps.length; i++) {
    let map = d3.select(votationMaps[i]);

    drawMap(map, vm);

    document.getElementById('toggleCanton')
      .addEventListener('click', (event) =>  map.node().classList.toggle('noCantons'));

    setInterval(function() {
      updateCantons(map.attr('data-votation-id'), vm);
      updateAllCommunes(map.attr('data-votation-id'), vm);
    }, 1000);

    updateCantons(map.attr('data-votation-id'), vm);
    updateAllCommunes(map.attr('data-votation-id'), vm);
  }

});

