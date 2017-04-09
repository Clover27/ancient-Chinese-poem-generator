var app = new Vue({
  el: '#root',
  data: {
    sentence: '',
    prime: '',
    show: false
  },
  methods: {
    checkSentence: function () {
      if (this.sentence.trim() == '') {
        $('#sentence').popup('show')
        setTimeout(function () {
          $('#sentence').popup('hide')
        }, 5000)
        return false
      } else {
        return true
      }
    },
    checkPrime: function () {
      if (this.prime.trim() == '') {
        $('#prime').popup('show')
        setTimeout(function () {
          $('#prime').popup('hide')
        }, 5000)
        return false
      } else {
        return true
      }
    },
    doit: function () {
      let b = this.checkSentence()
      let me = this
      if (b) {
        $('#root .pg-output li').remove()
        me.show = true
        let url = '/generate?sentence=' + this.sentence.trim() + '&prime=' + this.prime.trim()
        $.getJSON(url, function (data) {
          me.show = false
          if (!data || !data.result || data.result.length < 1) {
            $('#root .pg-output').append('<li style="letter-spacing:1px;">Failed to generate poem.</li>')
            return
          }
          for (let i = 0; i < data.result.length; i++) {
            let len = data.result[i].length
            let end = i == data.result.length - 1 ? '。' : '，'

            insert(i, data.result[i] + end, i * (len + 3) * 300)
          }

          function insert(index, line, delay) {
            setTimeout (function () {
              $('#root .pg-output').append('<li class="tlt' + index + '">' + line + '</li>')
              $('.tlt' + index).textillate({ 
                in: { 
                  effect: 'fadeIn',
                  delay: 300
                } 
              })
            }, delay)
          }
        })
        .fail(function () {
          me.show = false
          $('#root .pg-output').append('<li style="letter-spacing:1px;">Failed to generate poem.</li>')
        })
      }
    }
  },
  mounted: function () {
    this.$nextTick(function () {
      $('#sentence')
        .popup({
          content: 'Please type the first sentence',
          variation: 'inverted',
          on: 'manual'
        })
      $('#prime')
        .popup({
          content: 'Please type the prime keyword',
          variation: 'inverted',
          on: 'manual'
        })
    })
  }
})