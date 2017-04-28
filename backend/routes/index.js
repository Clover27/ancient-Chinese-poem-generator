var express = require('express');
var router = express.Router();
const exec = require('child_process').exec
const path = require('path')

const generate = path.resolve('../lstm/generate.py')
const vocabulary = path.resolve('../model/weights-500-3-0.2/vocabulary.json')
const weights = path.resolve('../model/weights-500-3-0.2/weights-improvement-174-2.9403.hdf5')
const model = path.resolve('../model/weights-500-3-0.2/model-500-3-0.2.h5')

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/generate', function(req, res, next) {
  let sentence = req.query.sentence.trim()
  let prime = req.query.prime.trim()
  let primeCommand = prime ? (' -p ' + prime) : ''
  let command = 'python3 ' + generate + primeCommand + ' -s ' + sentence + ' -v ' + vocabulary + ' -w ' + weights + ' -m ' + model
  
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      res.json({
        result: []
      })
      return;
    }
    console.log(`stdout:\n ${stdout}`);
    stderr && console.log(`stderr: ${stderr}`);

    if (stdout && stdout !== '') {
      let arr = stdout.split('\n')
      arr.splice(arr.length - 1, 1)
      arr.forEach((value, index, array) => {
        arr[index] = arr[index].trim()
      })

      res.json({
        result: arr
      })
    } else {
      res.json({
        result: []
      })
    }
  })
});

module.exports = router;
