document.addEventListener('alpine:init', () => {
    Alpine.data('construction', () => {
        return {
            Delay: '' ,
            laborers: '' ,
            cash_flow: '' ,
            Errors: '' ,
            communication: '' ,
            Change_schedule: '' ,
            bid_price: '' ,
            scope_change: '' ,
            Weather_conditions: '' ,
            Accidents: '' ,

            hist: [],
            predicted: '',
            show_prediction: '',

            init() {
                // this.getHistory();
                console.log('Connected...')
            },

            getHistory() {
                axios.get('/api/historical_data/')
                    .then((response) => {
                        this.hist = response.data.historical_data;
                        console.log(response.data);
                    })
            },

            MakePrediction() {
                axios.post('/predict', {
                    laborers: this.laborers,
                    cash_flow: this.cash_flow,
                    Errors: this.Errors ,
                    communication: this.communication ,
                    Change_schedule: this.Change_schedule ,
                    bid_price: this.bid_price ,
                    scope_change: this.scope_change ,
                    Weather_conditions: this.Weather_conditions ,
                    Accidents: this.Accidents
                })
                .then((response) => {
                    // this.getHistory();
                    this.predicted = response.data.prediction;
                    this.show_prediction = 'Predicted value is: ' + response.data.prediction;
                    console.log(response.data);
                })
           
                
            }




        }

    })
})