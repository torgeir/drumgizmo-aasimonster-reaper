#coding: utf-8
require 'rexml/document'
require 'fileutils'


# ruby extract.rb ./MT-PowerDrumKit.dll ./midi

dll = ARGV[0]
dest = ARGV[1]

data= IO.read('MT-PowerDrumKit.dll', :encoding=>'ascii-8bit')

xml_start = data.index('<GrooveDef')
xml_end = data.index('</GrooveDef>')+'</GrooveDef>'.length
xml = data[xml_start..xml_end]

data_start = xml_end+2

doc = REXML::Document.new(xml)
root = doc.root
root.elements.each("SuperStyle") do |ss|
  ss.elements.each("Style") do |s|
    s.elements.each("Groove") do |g|
      n_g = g.attributes["Name"].gsub("/","_")

      path = File.join([dest] + [ss, s, g].map{|e| e.attributes["Name"].gsub("/","_")})
      FileUtils.mkdir_p(path)
      offset = g.attributes["Offset"].to_i
      size = g.attributes["Size"].to_i
      File.open(File.join(path, n_g)+".mid","w"){|fil| fil.write(data[data_start+offset, size])}
      g.elements.each("Fill") do |f|
        n_f = f.attributes["Name"].gsub("/","_")
        offset = f.attributes["Offset"].to_i
        size = f.attributes["Size"].to_i
        File.open(File.join(path, n_f)+".mid","w"){|fil| fil.write(data[data_start+offset, size])}
      end
    end
  end
end


